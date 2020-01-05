import re 
import os
import unidecode # transliterates special characters
from mutagen.id3 import ID3, APIC, TT2, TPE1, TRCK, TALB, USLT, error

class Clean():
    def __init__(self, fname):
        id3 = ID3(f'test/{fname}')
        # print([i for i in id3])

        self.lyrics = ""
        if "USLT::eng" in id3:
            self.lyrics = id3["USLT::eng"]
        elif "USLT::XXX" in id3:
            self.lyrics = id3["USLT::XXX"]
        
        self.album = id3["TALB"] if "TALB" in id3 else ""
        self.artist = id3["TPE1"] if "TPE1" in id3 else ""
        self.title = id3["TIT2"] if "TIT2" in id3 else ""
        self.cover = id3["APIC:"] if "APIC:" in id3 else ""

        if not self.title or not self.artist:
            fname = fname.lower().replace(".mp3", "")
            rem = ["official", "oficial", "audio", "lyrics", "lyric", "video"]
            for i in rem:
                fname = fname.replace(i, "") if i in fname else fname
            fname = re.sub("\s[^a-z\-]", "", fname).split("-")

            if not self.title:
                self.title = fname[0].strip().title()
            if not self.artist:
                try:
                    self.artist = fname[1].strip().title()
                except:
                    pass
            

    def retrieve(self):
        print(f"Album: {unidecode.unidecode(str(self.album))}"
              f"\nArtist: {unidecode.unidecode(str(self.artist))}"
              f"\nTitle: {unidecode.unidecode(str(self.title))}"
              f"\nLyrics: {unidecode.unidecode(str(self.lyrics))[:20]}")


    def create_json(self):
        pass

    def export_json(self):
        pass

        # ID3 info:
        # APIC: picture
        # TT2 (TIT2): title
        # TPE1: artist
        # TRCK: track number
        # TALB: album
        # USLT: lyric

if __name__ == "__main__":
    
    for fname in os.listdir("test/"):
        if ".mp3" in fname:
            Clean(fname).retrieve()
            print("\n")
            
            # fname_uni = unidecode.unidecode(fname)
            # artist, title = Clean(fname_uni).retrieve()
            # print(f"Artist: {artist}")
            # print(f"Title: {title}")
            # print()
    # me = ""
    # if not me:
    #     print("im alive")
    # else:
    #     print("im never here")