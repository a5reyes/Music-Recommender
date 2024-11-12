# Music-Recommender
website: https://reyesalbert34.pythonanywhere.com/
#### ***DATED*** Video Demo: https://www.youtube.com/watch?v=aXGe6ySl05Y
#### Description:
Using Spofity APIs and Flask,
this is a music recommender based on input of the user
already likes such as: a song, an album and artist
but, if the user chooses genre, it gives a random genre with its top artists.
For song or album: the program will be getting a simiar song or album by an artist
or just an artist from the user's input then using spofity's various recommendations features through spotipy,
(aka the "Recommended" feature for songs and the "Fans also like" feature for artist) to return similar songs,
albums or artists regardless of whether or not textcase or punctuation is in user's items.

#### Important edge cases: - 19 by adele - 4 by beyonce - you'd prefer an astronaut by hum - spiderland by slint
These four albums and their artists' name are the four edge cases that led me to make
the search_artist, albums_by_artist, check_popularity, check_artist_name, artist_id methods,
four methods that I found very important in order for this whole program to run efficiently.
These artists (and also their albums) vary greater in popularity
but what they have in common are their artist and album names.
At first, because artists like hum, slint, adele and beyonce have such short/simple but mysterious names,
my program would recommened less popular artists and their albums
or sometimes, especially in the case of more obscure artists like hum or slint,
my program would return different more popular but unrelated artists and their albums.
So, i made the search artist and check popularity methods to handle both of these different types of edges cases
in terms of getting exactly what the user inputtted and getting right recommendations for the user.
In the case of 19 by adele and 4 by beyonce, it was getting the right artists,
using my search_artist method to search and get the first artist in the query,
checking that first initial artist's name in the query against the name inputted by the user despite textcase
(or in the case of beyonce, despite accents: using unidecode because beyonce has an accent in her name on the last e letter.)
If the initial artist's (from the query of the first search) name doesn't match with the name from the user,
it uses the check_artist_name method to get all the names of all the artists from the search query
and gets the most popular artist which will most likely be the same artist as the one inputted by the user in the first place.
In the case of the album you'd prefer an astronaut by Hum (one of my favorite bands),
the apostrophe caused an error in my program so I made a titlecase method using regex to handle cases of items with apostrophes.
I also used titlecase in conjunction with casefold to handle stylized artist names like girl in red or MGMT
and also artists who love to stylize their discography using textcase like BROCKHAMPTON or Billie Eilish.
