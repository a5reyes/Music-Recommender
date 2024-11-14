import unittest
import project as project

class TestMusicRecommendations(unittest.TestCase):
    def setUp(self):
        self.original_main = project.main

    def tearDown(self):
        project.main = self.original_main

    def test_song(self):
        test_songs = {
            "imgonnagetyouback": "Taylor Swift",
            "i": "Kendrick Lamar",
            "You Might Think He Loves You for Your Money but I Know What He Really Loves You for": "Death Grips",
            "19-2000": "Gorillaz",
            "C.R.E.A.M.": "Wu-Tang Clan",
            "?": "MF DOOM",
            "Untitled": "dangelo", #song stylized "Untitled (How Does It Feel)", artist stylized "D'angelo"
            "715 - CR∑∑KS": "Bon Iver",
            "There's a Good Reason These Tables Are Numbered Honey, You Just Haven't Thought of It Yet": "panic at the disco", #artist name stylized "Panic! At The Disco"
            "BAD GUY": "billie eilish" #song stylized "bad guy"
        }
        for song, artist in test_songs.items():
            project.main = lambda: "track"
            result = project.just_like_track(song, artist)
            self.assertIsNotNone(f"{result}")

    def test_album(self):
        test_albums = {
            "4": "beyonce", #artist name stylized "Beyoncé"
            "19": "adele", #artist name stylized "Adele"
            "I Like It When You Sleep, for You Are So Beautiful Yet So Unaware of It": "The 1975"
        }

        for album, artist in test_albums.items():
            project.main= lambda: "album"
            result = project.just_like_album(album, artist)
            self.assertIsNotNone(f"{result}")

    def test_artist(self):
        test_artists = [
            "suicideboys", #artist name stylized "$uicideboy$"
            "MGMT",
            "brockhampton", #artist name stylized "BROCKHAMPTON"
            "girl in red",
            "dangelo", #artist name stylized "D'Angelo"
            "R.E.M.",
            "!!!",
            "sunn o)))", #artist name stylized "sunn O)))"
            "Blue Öyster Cult",
        ]
        for artist in test_artists:
            project.main = lambda: "artist"
            band = project.search_artist(artist)
            self.assertIsNotNone(f"{band}", f"Expected a result for artist '{artist}'")
            if band:
                recommendations = project.get_artists_recs(band)
                self.assertIsNotNone(f"{recommendations}")

if __name__ == "__main__":
    unittest.main()
