# from mutagen.mp3 import MP3
# from mutagen.id3 import ID3, APIC, TT2, TPE1, TRCK, TALB, USLT, error
# # ID3 info:
# # APIC: picture
# # TT2: title
# # TPE1: artist
# # TRCK: track number
# # TALB: album
# # USLT: lyric

# pic_file = 'test/cat.jpg' # pic file
# imagedata = open(pic_file, 'rb').read()

# id3 = ID3('test/Clueless.mp3')
# id3.add(APIC(3, 'image/jpeg', 3, 'Front cover', imagedata))
# id3.add(TT2(encoding=3, text='title'))

# id3.save(v2_version=3)

import os
import unidecode # transliterates special characters
# import glob # pick out mp3 files
import re 

class Clean():
    def __init__(self, fname): # input is file audio
        # print(f"Original: {fname}")

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

        return artist.strip(), title.strip()


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import time

import requests
import urllib, json

class Search():
    def __init__(self, artist, title):
        self.artist = artist
        self.title = title

        self.driver = webdriver.Chrome()
        # self.options = Options()
        # self.options.add_argument("headless")
        # self.driver = webdriver.Chrome(executable_path='chromedriver', options=self.options)

    def retrieve(self):
        self.driver.get("http://www.google.com/")
        self.lyrics()
        self.album()
        self.cover()
        self.driver.close()

    def album(self):
        search = self.driver.find_element_by_name('q')
        search.clear()
        search.send_keys(f"album {self.artist} {self.title}")
        search.send_keys(Keys.RETURN)
        time.sleep(1)

        try:
            self.album = self.driver.find_element(By.CLASS_NAME, "Z0LcW").text
            self.album_uni = urllib.parse.quote(self.album.encode('utf8')) # encode spec char for url compatibility
        except:
            print("Either I choked or there is no album.")
        
    def cover(self):
        with open("api_keys.txt", "r") as f:
            api = f.readline().strip()
            uri = "http://ws.audioscrobbler.com"
            query = f"/2.0/?method=album.getinfo&api_key={api}&artist={self.artist}&album={self.album_uni}&format=json"

            response = urllib.request.urlopen(uri + query)
            data = json.loads(response.read())
            link = data["album"]["image"][5]["#text"]
            urllib.request.urlretrieve(link, f"covers/{self.album}.png")
            # print(json.dumps(data, indent=4, sort_keys=True))

    def lyrics(self):        
        # driver.execute_script("window.open('http://www.google.com/');")
        # driver.switch_to.window(driver.window_handles[1])
        search = self.driver.find_element_by_name('q')
        search.clear()
        search.send_keys(f"lyrics {self.artist} {self.title}")
        search.send_keys(Keys.RETURN)
        time.sleep(1)

        try:
            with open(f"lyrics/{self.artist} - {self.title}.txt", "w") as f:
                more = self.driver.find_element(By.CLASS_NAME, "vk_ard")
                more.click()
                for i in self.driver.find_elements(By.CSS_SELECTOR, 'div[jsname="U8S5sf"]'):
                    for elem in i.find_elements(By.CSS_SELECTOR, 'span[jsname="YS01Ge"]'):
                        if elem.text: # sometimes there are empty div
                            f.write(f"{unidecode.unidecode(elem.text)}\n")
                    f.write(f"\n")
        except:
            print("Either I choked or there are no lyrics.")

        # driver.get_screenshot_as_file("capture.png")

if __name__ == "__main__":
    # path, dirs, files = os.walk("test/").__next__()
    # for i in range(len(files) - 3):

    # for fname in os.listdir("test/"):
    #     if ".mp3" in fname:
    #         fname = unidecode.unidecode(fname)
    #         artist, title = Clean(fname).retrieve()
    #         print(f"Artist: {artist}")
    #         print(f"Title: {title}")
    #         print()

    # Search().album()
    Search("bich phuong", "chu meo").retrieve()
    Search("jaden", "summertime in paris").retrieve()
    Search("bratty", "honey no estas").retrieve()