import re 
import os
import json
import unidecode # transliterates special characters

from mutagen.id3 import ID3, ID3NoHeaderError


class Clean():
    def __init__(self, fname):
        # Ensure all mp3 files have an ID3 tag
        try:
            id3 = ID3(f'review/{fname}')
        except:
            id3 = ID3()
            
        self.fname = fname
        self.artist = id3["TPE1"] if "TPE1" in id3 else ""
        self.title = id3["TIT2"] if "TIT2" in id3 else ""
        self.album = id3["TALB"] if "TALB" in id3 else ""
        self.cover = id3["APIC:"] if "APIC:" in id3 else ""
        self.lyrics = ""

        if "USLT::eng" in id3:
            self.lyrics = id3["USLT::eng"]
        elif "USLT::XXX" in id3:
            self.lyrics = id3["USLT::XXX"]

        if not self.title or not self.artist:
            fname = fname.lower().replace(".mp3", "")
            rem = ["official", "oficial", "audio", "lyrics", "lyric", "video"]
            for i in rem:
                fname = fname.replace(i, "") if i in fname else fname
            fname = re.sub("\s[^a-z\-]", "", fname).replace(")", "").split("-")

            if not self.title:
                self.title = fname[0].strip().title()
            if not self.artist:
                try:
                    self.artist = fname[1].strip().title()
                except:
                    pass
            
    def result(self):
        return {"File": str(self.fname), "Artist": str(self.artist),
                "Title": str(self.title), "Album": str(self.album),
                "Lyrics": str(self.lyrics)}

    def debug(self):
        if self.artist:
            print("I got artist")
        if self.title:
            print("I got title")
        if self.album:
            print("I got album")
        if self.lyrics:
            print("I got lyrics")
        print(f"Artist: {unidecode.unidecode(str(self.artist))}"
              f"\nTitle: {unidecode.unidecode(str(self.title))}"
              f"\nAlbum: {unidecode.unidecode(str(self.album))}"
              f"\nLyrics: {unidecode.unidecode(str(self.lyrics))[:20]}")


class GetJson():
    def __init__(self, folder, reset=True):
        # Reset previous data
        if reset and os.path.exists("songs.json"):
            os.remove("songs.json")

        # Initiate list of songs
        try:
            with open('songs.json') as infile:
                songs = json.load(infile)
        except:
            songs = []

        # Perform clean on each file within dir
        for fname in os.listdir(folder):
            if ".mp3" in fname:
                songs.append(Clean(fname).result())

        # Output
        with open('songs.json', 'w') as outfile:
                json.dump(songs, outfile, indent=4)


if __name__ == "__main__":
    GetJson(reset=True)

    # ID3 info:
    # APIC: picture
    # TT2 (TIT2): title
    # TPE1: artist
    # TRCK: track number
    # TALB: album
    # USLT: lyric