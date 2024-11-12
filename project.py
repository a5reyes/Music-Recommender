import random
import re
import string
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from unidecode import unidecode

client_id = "..."
client_secret = "..."
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

#intro
def main():
    res = input("Hello, looking for music?  Choose one category: track, album, artist, genre  -  ")
    get_info(res)

#determining what the user input is; whether it is a track, album, etc.
def get_info(category):
    if category in ["artist"]:
        print("Enter what you already like")
        user_input = input("What artist? ")
        artist = search_artist((titlecase(user_input)).casefold())
        if artist:
            recs = get_artists_recs(artist)
            return recs
        else:
            return f"Can't find {user_input}"
    elif category in ["track"]:
        print("Enter what you already like")
        user_input = input("What track? ")
        user_artist = input("By what artist? ")
        recs = just_like_track(user_input, user_artist)
        return recs
    elif category in ["album"]:
        user_input = input("What album? ")
        user_artist = input("By what artist? ")
        recs = just_like_album(titlecase(user_input), titlecase(user_artist).casefold())
        return recs
    elif category in ["genre"]:
        genres = just_like_genre()
        return genres
    else:
        return "Invalid category: please enter either artist, track, album, genre"


#searching for artist and getting artist id for recommendations
def search_artist(name):
    global artist_info
    results = sp.search(q=f"{name}", type="artist")
    items = results["artists"]["items"]
    initial_artist = items[0]
    initial_artist_name = unidecode(initial_artist.get('name')).casefold() #to handle artist names with accents
    first_artist_name = initial_artist_name.translate(str.maketrans('', '', string.punctuation)) #to handle artist names with punctuation, etc.
    if initial_artist_name == name or first_artist_name == name or first_artist_name in name:
        pop_rating = initial_artist.get('popularity', 0)
        pop = int(pop_rating)
        artist_id = initial_artist.get('id')
        band_id = get_artist_id(name)
        if pop > 30 and artist_id == band_id[0]:
            return initial_artist
    bands = check_artist_name(items, name) #if artist name is not the same as the initial artist retrieved int the first search query
    for band in bands:
        artist_info = band
        artist_popularity = artist_info.get('popularity', 0)
        popularity = int(artist_popularity)
        if popularity > 30:
                return artist_info #returning artist info
        else:
            return check_popularity(name) #for obscure artists
    if len(items) == 0:
        pass

#track recommendations
def just_like_track(song, band):
    recs = []
    results = sp.search(q=f"artist:{band} track:{song}", limit=1, type="track")
    if results["tracks"]["items"]:
        recommends = sp.recommendations(seed_tracks=[results["tracks"]["items"][0]["id"]], limit=10)
        for track in recommends["tracks"]:
            recs.append("- {} by {}".format(track["name"], ", ".join([artist["name"] for artist in track["artists"]])))
        return [rec for rec in recs]
    else:
        return f"Can't find {titlecase(song)} by {titlecase(band)}"

#album recommendations
def just_like_album(release, group):
    recs = []
    artist = search_artist(group)
    if artist:
        check_album = albums_by_artist(artist)
        discography = [album.translate(str.maketrans('', '', string.punctuation)) for album in check_album] #for albums with punctuation, etc.
        if release in discography or any(release in album for album in discography) and [release in album for album in discography]: #if album is indeed in artist's discography
            rec_artists = get_albums_recs(artist)
            while rec_artists is None:
                try:
                    rec_artists = get_albums_recs(artist)
                except TypeError:
                    continue
            for recs_artist in rec_artists:
                band = search_artist(recs_artist)
                if band is None:
                    continue
                if band:
                    try:
                        results = sp.artist_albums(band["id"], album_type="album")
                        albums = results["items"]
                        while results["next"]:
                            results = sp.next(results)
                            albums.extend(results["items"])
                        for album in random.choices(albums):
                            if len(band['genres']) != 0:
                                album_info = f"- {album['name']} by {band['name']} - Genre: {band['genres']}"
                                recs.append(album_info)
                            else:
                                continue
                    except IndexError:
                        continue
            return recs
        else:
            return f"{titlecase(release)} not by {titlecase(group)}"
    else:
        return f"Can't find {titlecase(group)}"

#getting artists recommendations
def get_artists_recs(var):
    recs= []
    recommends = sp.recommendations(seed_artists=[var["id"]], limit=10)
    for track in recommends["tracks"]:
        recommends_list = [artist["name"] for artist in track["artists"]]
        if var["name"] in recommends_list:
            continue
        else:
            recs.append(f"- {recommends_list[0]}")
    return recs 

#getting artist recs and putting them into list for album recs
def get_albums_recs(variable):
    recommends = sp.recommendations(seed_artists=[variable["id"]], limit=10)
    artist_names = []
    for track in recommends["tracks"]:
            artist_names.append(" ".join([artist["name"] for artist in track["artists"]]))
    if variable['name'] in artist_names:
        return artist_names.remove(variable['name'])
    return artist_names

#to check if said album is indeed by the artist
def albums_by_artist(project):
    results = sp.artist_albums(project["id"], album_type="album")
    albums = results["items"]
    albums_names = []
    while results["next"]:
        results = sp.next(results)
        albums.extend(results["items"])
    for album in albums:
        name = album["name"]
        release_name = name.split('(')[0].strip()  #for albums listed as deluxe or collector's edition, etc.
        albums_names.append(titlecase(release_name))
    return albums_names

#random genre and top artists of said random genre
def just_like_genre():
    recs=[]
    genres = sp.recommendation_genre_seeds()
    genres_list = list(genres.values())
    rand_genre = random.choice(genres_list[0])
    genre = sp.search(q=f"genre: {rand_genre}", type='artist', limit=5)
    top_artists = [artist['name'] for artist in genre['artists']['items']]
    for artist in top_artists:
        recs.append(f"{titlecase(rand_genre)}: Top Artists- {artist}")
    return recs 

#check popularity for obscure artists
def check_popularity(band):
    global unique_artist
    results = sp.search(q=f"artist:{band}", limit=5, type="artist")
    artists_info = list(results.values())
    artists = artists_info[0]
    multi_artists = artists.get('items')
    for artist in multi_artists:
        pop_rating = artist.get('popularity')
        popularity_rating = int(pop_rating)
        if popularity_rating > 0:
            unique_artist = []
            unique_artist.append(artist)
    if len(unique_artist) > 0:
        return unique_artist[0]
    else:
        return None

#turning all artists names retrieved from search query and putting them into a list; artist name checker
def check_artist_name(items, band_name):
    result = []
    for item in items:
        name_checker = item.get('name')
        if name_checker == titlecase(band_name):
            result.append(item)
    return result

#getting artist id for verifying artist through album recs
def get_artist_id(singer):
    results = sp.search(q=f"{singer}", limit=5, type="artist")
    artists_info = list(results.values())
    artists = artists_info[0]
    multi_artists = artists.get('items')
    res = sp.search(q=f"{singer}", type="artist")
    items = res["artists"]["items"]
    initial_artist = items[0]
    initial_artist_id = initial_artist.get('id')
    actual_artist_id = []
    for artist in multi_artists:
        artist_id = artist.get('id')
        if artist_id == initial_artist_id:
            actual_artist_id.append(artist_id)
        else:
            continue
    return actual_artist_id

#for textcase and special characters in edge cases
def titlecase(s):
    return re.sub(r"[^\W\d_]+(?:['’][^\W\d_]+)?", lambda mo: mo.group(0).capitalize(), s)

if __name__ == "__main__":
    main()
