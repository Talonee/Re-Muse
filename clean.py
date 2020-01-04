import re 

class Clean():
    def __init__(self, fname): # input is file audio
        # Remove misc
        self.fname = fname.lower().replace(".mp3", "")
        self.rem = ["official", "oficial", "audio", "lyrics", "lyric", "video"]
        for i in self.rem:
            self.fname = self.fname.replace(i, "") if i in self.fname else self.fname
        self.fname = re.sub("\s[^a-z\-]", '', self.fname)

    def retrieve(self):
        print(f"Modified: {self.fname}")
        artist = self.fname.split("-")[0]
        try:
            title = self.fname.split("-")[1]
        except:
            title = ""

        return artist.strip().title(), title.strip().title()

    def create_json(self):
        pass

    def export_json(self):
        pass
