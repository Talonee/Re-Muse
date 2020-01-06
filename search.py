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

import webbrowser

import clean

class Search():
    def __init__(self, song):
        self.fname = song["File"]
        self.artist = song["Artist"]
        self.title = song["Title"]
        self.lyrics = song["Lyrics"]
        self.album = song["Album"]
        self.cover = ""

        self.driver = webdriver.Chrome()
        # self.options = Options()
        # self.options.add_argument("headless")
        # self.driver = webdriver.Chrome(executable_path='chromedriver', options=self.options)

    def do_something(self):
        self.driver.get("http://www.google.com/") # get u a window
        self.get_lyrics() # do ya thang
        self.driver.close() # closing it now

    # This boy got recursion
    # This method is needed when a song doesn't have lyrics (i.e Flume - Helix)
    def get_song(self, arg1=None, arg2=None, rerun=True):
        if not arg1 and not arg2:
            arg1 = self.title
            arg2 = self.artist 
            
        search = self.driver.find_element_by_name('q')
        search.clear()
        search.send_keys(f"artist {arg1} {arg2}")
        search.send_keys(Keys.RETURN)
        time.sleep(0.5)

        try:
            self.artist = self.driver.find_element(By.CLASS_NAME, "Z0LcW").text
            self.title = self.driver.find_element(By.CSS_SELECTOR, 'span[class="GzssTd"]').text 
        except:
            try:
                self.artist = self.driver.find_element(By.CSS_SELECTOR, 'div[class="title"]').text
                self.title = self.driver.find_element(By.CSS_SELECTOR, 'span[class="kxbc"]').text
            except:
                if rerun:
                    self.get_song(self.artist, self.title, False)
                pass
        
    def get_lyrics(self):
        search = self.driver.find_element_by_name('q')
        search.clear()
        search.send_keys(f"lyrics {self.title} {self.artist}")
        search.send_keys(Keys.RETURN)
        time.sleep(0.5)

        try:
            more = self.driver.find_element(By.CLASS_NAME, "vk_ard")
            more.click()

            texts = []
            for i in self.driver.find_elements(By.CSS_SELECTOR, 'div[jsname="U8S5sf"]'):
                for elem in i.find_elements(By.CSS_SELECTOR, 'span[jsname="YS01Ge"]'): 
                    if elem.text: # sometimes there are empty div
                        texts.append(f"{elem.text}\n")
                texts.append("\n")

            self.lyrics = "".join(texts).replace("\n\n\n", "\n\n") # remove any double line break
        except:
            pass

        try:
            self.artist = self.driver.find_element(By.XPATH, '/html/body/div[8]/div[3]/div[10]/div[1]/div[2]/div/div[2]/div[2]/div/div/div[1]/div/div[1]/div[1]/span/div/div/div[1]/div[2]/div/div/div/div[2]/span').text
            self.title = self.driver.find_element(By.CSS_SELECTOR, 'div[data-attrid="title"]').text
        except:
            self.get_song()

        print(f"Artist: {unidecode.unidecode(self.artist)}\n"
              f"Title: {unidecode.unidecode(self.title)}\n"
              f"Lyrics: {True if self.lyrics else False}\n")

    def get_cover(self):
        pass



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

        self.album_uni = urllib.parse.quote(self.album.encode('utf8')) # encode spec char for url compatibility


    def cover(self):
        try: #Try to acces last.fm's API
            # Download cover art from Last.fm's API
            with open("api_keys.txt", "r") as f:
                api = f.readline().strip()
                uri = "http://ws.audioscrobbler.com"
                query = f"/2.0/?method=album.getinfo&api_key={api}&artist={self.artist}&album={self.album_uni}&format=json"

                response = urllib.request.urlopen(uri + query)
                data = json.loads(response.read())
                link = data["album"]["image"][5]["#text"]
                urllib.request.urlretrieve(link, f"covers/{self.album}.jpg")

            # Google Reverse Image Search
            filePath = f'covers/{self.album}.jpg'
            searchUrl = 'http://www.google.hr/searchbyimage/upload'
            multipart = {'encoded_image': (filePath, open(filePath, 'rb')), 'image_content': ''}
            response = requests.post(searchUrl, files=multipart, allow_redirects=False)
            fetchUrl = response.headers['Location']
            self.driver.get(fetchUrl)

            try:
                img_size = self.driver.find_element(By.XPATH, "/html/body/div[8]/div[3]/div[3]/div[1]/div[2]/div/div[2]/div[1]/div/div[1]/div[2]/div[2]/span[4]/a")
            except:
                img_size = self.driver.find_element(By.XPATH, "/html/body/div[8]/div[3]/div[3]/div[1]/div[2]/div/div[2]/div[1]/div/div[1]/div[2]/div[2]/span[3]/a")
            img_size.click()

        except: # No album available, go to google search
            self.driver.get("https://images.google.com/")
            search = self.driver.find_element_by_name('q')
            search.clear()
            search.send_keys(f"album {self.artist} {self.title}")
            search.send_keys(Keys.RETURN)

        # Select img size and search result
        # res = self.driver.find_element(By.CLASS_NAME, 'rg_i') # first result
        res = self.driver.find_element(By.XPATH, '/html/body/div[7]/div[3]/div[3]/div[2]/div/div[2]/div[2]/div/div/div/div/div[2]/div[1]/div[1]/a[1]/img') # first result
        res.click()
        enlarged = self.driver.find_element(By.XPATH, "//*[@id='irc-ss']/div[2]/div[1]/div[4]/div[1]/a/div/img").get_attribute('src') # retrieve image src
        # enlarged = self.driver.find_element(By.XPATH, "/html/body/div[2]/c-wiz/div[3]/div[2]/div[2]/div/div/div[3]/div[2]/div/div[1]/div[1]/div/div[2]/a/img").get_attribute('src') # retrieve image src
        
        # Download img while bypassing http forbidden response (403) using user-agent
        opener = urllib.request.build_opener() 
        opener.addheaders = [('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
        urllib.request.install_opener(opener)
        urllib.request.urlretrieve(enlarged, f"covers/{self.album}.jpg")


    def lyrics(self):
        search = self.driver.find_element_by_name('q')
        search.clear()
        search.send_keys(f"lyrics {self.artist} {self.title}")
        search.send_keys(Keys.RETURN)
        time.sleep(1)

        try:
            more = self.driver.find_element(By.CLASS_NAME, "vk_ard")
            more.click()

            texts = []
            for i in self.driver.find_elements(By.CSS_SELECTOR, 'div[jsname="U8S5sf"]'):
                for elem in i.find_elements(By.CSS_SELECTOR, 'span[jsname="YS01Ge"]'): 
                    if elem.text: # sometimes there are empty div
                        texts.append(f"{elem.text}\n")
                texts.append("\n")

            self.lyrics = "".join(texts).replace("\n\n\n", "\n\n") # remove any double line break

        except:
            print("Either I choked or there are no lyrics.")

        # driver.get_screenshot_as_file("capture.png")

    def modify(self):
        # ID3 info:
        # APIC: picture
        # TT2: title
        # TPE1: artist
        # TRCK: track number
        # TALB: album
        # USLT: lyric

        cover = open(f"covers/{self.album}jj.jpg", 'rb').read()

        id3 = ID3(f'test/{self.fname}')
        id3.add(APIC(3, 'image/jpeg', 3, 'Cover', cover))
        id3.add(TT2(encoding=3, text=f"{self.title}"))
        id3.add(TPE1(encoding=3, text=f"{self.artist}"))
        id3.add(TALB(encoding=3, text=f"{self.album}"))


        # Lyrics
        try: # try to get XXX lyrics
            if id3["USLT::XXX"] and id3["USLT::XXX"] == "": # if exists but empty
                id3.add(USLT(encoding=3, text=f"{self.lyrics}"))
            # else, prob not empty, leave it
        except: # no X, try eng
            try:    
                if id3["USLT::eng"] and id3["USLT::eng"] == "": # if exists but empty
                    id3.add(USLT(encoding=3, text=f"{self.lyrics}"))
                # else, prob not empty, leave it
            except:
                # no lyrics, add
                id3.add(USLT(encoding=3, text=f"{self.lyrics}"))

        try:
            print(str(id3["USLT::eng"])[3], self.artist)
        except:
            print(str(id3["USLT::XXX"])[3], self.artist)

        id3.save(v2_version=3) # save

    def rename(self):
        os.rename('guru99.txt','career.guru99.txt') 


if __name__ == "__main__":
    with open('songs.json') as infile:
        songs = json.load(infile)

    for song in songs:
        Search(song).do_something()



    # for fname in os.listdir("test/"):
    #     if ".mp3" in fname:
    #         fname_uni = unidecode.unidecode(fname)
    #         artist, title = Clean(fname_uni).retrieve()
    #         print(f"Artist: {artist}")
    #         print(f"Title: {title}")
    #         print()

    #         Search(artist, title, fname).retrieve()

    # print(urllib.parse.quote("Tóc Tiên".encode('utf8')))
        # cover = open(f"covers/jj.jpg", 'rb').read()

        # id3 = ID3(f'test/sample.mp3')
        # # id3.delete()
        # for i in id3:
        #     print(i)
        # # id3["APIC:Cover"] = APIC(3, 'image/jpeg', 3, 'Cover', cover)
        # # id3["APIC"] = APIC(3, 'image/jpeg', 3, 'Cover', cover)
        # id3.add(APIC(3, 'image/jpeg', 3, 'Cover', cover))
        # # del id3["APIC:Cover"]
        # print("NEW LINE")
        # for i in id3:
        #     print(i)
        # # id3.add(TT2(encoding=3, text=f"{self.title}"))
        # # id3.add(TPE1(encoding=3, text=f"{self.artist}"))
        # # id3.add(TALB(encoding=3, text=f"{self.album}"))
        # id3.save(v2_version=3) # save
    # lyr = mutagen.File("test/Jaden - GOKU.mp3")["USLT::XXX"]
    # lyr = mutagen.File("Xin Lỗi Anh Quá Phiền.mp3")["USLT::XXX"]
    # if lyr:
    #     print("I'm in")
        # ID3 info:
        # APIC: picture
        # TT2: title
        # TPE1: artist
        # TRCK: track number
        # TALB: album
        # USLT: lyric

    # me = mutagen.File("Louis The Child - Better Not (Lyric Video) ft. Wafia.mp3")

    # for i in mutagen.File("Louis The Child - Better Not (Lyric Video) ft. Wafia.mp3"):
    #     print(i)
    # print("\n\n")

    # id3 = ID3(f'Có ai thương em như vậy.mp3')
    # # id3.add(USLT(encoding=3, text=""))
    # id3.save(v2_version=3)
    # for i in id3:
    #     print(i)

    # print(str(id3["USLT::eng"])[3])
    # if id3["USLT::XXX"] == "":
    #     print("Empty")
    # else:
    #     print("Not empty")




    # for i in mutagen.File("Louis The Child - Better Not (Lyric Video) ft. Wafia.mp3"):
    #     print(i)

    # print(mutagen.File("Louis The Child - Better Not (Lyric Video) ft. Wafia.mp3")["USLT::XXX"])
            #if no eng, then no lyrics exist, proceed to add.
    #         Search(artist, title, fname).retrieve()
