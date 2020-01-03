from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, TT2, TPE1, TRCK, TALB, USLT, error


import os
import unidecode # transliterates special characters
import re 

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import time

import requests
import urllib, json


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

        return artist.strip().title(), title.strip().title()


class Search():
    def __init__(self, artist, title, fname):
        self.artist = artist
        self.title = title
        self.fname = fname

        self.driver = webdriver.Chrome()
        # self.options = Options()
        # self.options.add_argument("headless")
        # self.driver = webdriver.Chrome(executable_path='chromedriver', options=self.options)

    def retrieve(self):
        self.driver.get("http://www.google.com/")
        self.lyrics()
        self.album()
        self.cover()
        self.modify()
        self.driver.close()

    def album(self):
        search = self.driver.find_element_by_name('q')
        search.clear()
        search.send_keys(f"album {self.artist} {self.title}")
        search.send_keys(Keys.RETURN)
        time.sleep(1)

        try:
            self.album = self.driver.find_element(By.CLASS_NAME, "Z0LcW").text
        except:
            self.album = self.title
            print("Either I choked or there is no album.")

        self.album_uni = urllib.parse.quote(self.album.encode('utf8')) # encode spec char for url compatibility


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

        more = self.driver.find_element(By.CLASS_NAME, "vk_ard")
        more.click()

        texts = []
        for i in self.driver.find_elements(By.CSS_SELECTOR, 'div[jsname="U8S5sf"]'):
            for elem in i.find_elements(By.CSS_SELECTOR, 'span[jsname="YS01Ge"]'):
                if elem.text: # sometimes there are empty div
                    # f.write(f"{unidecode.unidecode(elem.text)}\n")
                    texts.append(f"{elem.text}\n")
            texts.append("\n")

        self.lyrics = "".join(texts).replace("\n\n\n", "\n\n") # remove any double line break

        # try:
        #     with open(f"lyrics/{self.artist} - {self.title}.txt", "w") as f:
        #         more = self.driver.find_element(By.CLASS_NAME, "vk_ard")
        #         more.click()
        #         for i in self.driver.find_elements(By.CSS_SELECTOR, 'div[jsname="U8S5sf"]'):
        #             for elem in i.find_elements(By.CSS_SELECTOR, 'span[jsname="YS01Ge"]'):
        #                 if elem.text: # sometimes there are empty div
        #                     # f.write(f"{unidecode.unidecode(elem.text)}\n")
        #                     f.write(f"{elem.text}\n")
        #             f.write(f"\n")
        # except:
        #     print("Either I choked or there are no lyrics.")

        # driver.get_screenshot_as_file("capture.png")

    def modify(self):
        # ID3 info:
        # APIC: picture
        # TT2: title
        # TPE1: artist
        # TRCK: track number
        # TALB: album
        # USLT: lyric

        cover = open(f"covers/{self.album}.png", 'rb').read()

        id3 = ID3(f'test/{self.fname}')
        id3.add(APIC(3, 'image/png', 3, 'Front cover', cover))
        id3.add(TT2(encoding=3, text=f"{self.title}"))
        id3.add(TPE1(encoding=3, text=f"{self.artist}"))
        id3.add(TALB(encoding=3, text=f"{self.album}"))
        id3.add(USLT(encoding=3, text=self.lyrics))

        id3.save(v2_version=3)

if __name__ == "__main__":
    # path, dirs, files = os.walk("test/").__next__()
    # for i in range(len(files) - 3):

    for fname in os.listdir("test/"):
        if ".mp3" in fname:
            fname_uni = unidecode.unidecode(fname)
            artist, title = Clean(fname_uni).retrieve()
            print(f"Artist: {artist}")
            print(f"Title: {title}")
            print()

    # Search().album()
            Search(artist, title, fname).retrieve()
    # Search("jaden", "summertime in paris").retrieve()
    # Search("bratty", "honey no estas").retrieve()