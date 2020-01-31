from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, TT2, TPE1, TRCK, TALB, USLT, error

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from PIL import Image

import os, shutil, unidecode, time, json, urllib.request, threading

import clean
# ID3 info:
# APIC: picture
# TT2: title
# TPE1: artist
# TRCK: track number
# TALB: album
# USLT: lyric

class Finalize():
    def __init__(self, jsonf):
        # self.driver = webdriver.Chrome()

        with open(jsonf) as infile:
            songs = json.load(infile)
        index = int(len(songs) / 2)
        
        thread1 = ReMuse(songs[:index])
        thread2 = ReMuse(songs[index:])

        thread1.start()
        thread2.start()
        thread1.join()
        thread2.join()

class ReMuse(threading.Thread):
    def __init__(self, songs):
        threading.Thread.__init__(self)

        self.songs = songs

    def run(self):
        self.options = Options()
        # self.options.add_argument("headless")
        self.options.add_argument("--incognito")
        self.options.add_argument("--mute-audio")
        self.driver = webdriver.Chrome(executable_path='chromedriver', options=self.options)
        self.driver.get("https://music.youtube.com/")
        self.driver.execute_script("window.open('http://www.google.com/');")

        for song in self.songs:
            # This is where the progress bar iterates
            Search(self.driver, song).find()
            mehoy = unidecode.unidecode(song["File"])
            print(f"Finished with {mehoy}")
        
        self.driver.quit()

class Search():
    def __init__(self, driver, song):
        self.driver = driver
        self.fname = song["File"]
        self.artist = song["Artist"]
        self.title = song["Title"]
        self.album = song["Album"]
        self.lyrics = song["Lyrics"]
        self.cover = ""

        self.success = True

    def find(self):    
        self.get_song()
        if self.valid:
            self.get_lyrics()
            self.finalize()

    def get_song(self, type="song"):
        self.driver.switch_to.window(self.driver.window_handles[0])

        # Click search button
        time.sleep(1)
        src_btn = self.driver.find_element(By.CSS_SELECTOR, 'ytmusic-search-box[role="search"]')
        src_btn.click()
        time.sleep(0.5)

        # Enter input
        search = self.driver.find_element(By.CSS_SELECTOR, 'input[id="input"]')
        search.clear()  
        search.send_keys(f"{self.title} {self.artist}")
        search.send_keys(Keys.RETURN)
        time.sleep(1.5)

        # Show song results only
        song_res = self.driver.find_element(By.CSS_SELECTOR, 'a[title="Show song results"]')
        song_res.click()
        time.sleep(0.75)

        # Locate title, check for the correct song
        self.loc_title = self.driver.find_element(By.XPATH, "/html/body/ytmusic-app/ytmusic-app-layout/div[3]/ytmusic-search-page/ytmusic-section-list-renderer/div[2]/ytmusic-shelf-renderer/div[1]/ytmusic-responsive-list-item-renderer[1]/div[2]/div[1]/yt-formatted-string").get_attribute("title")
  
        valid_check = f"{self.title} {self.artist} {self.album}".lower().split()

        self.valid = False
        for word in valid_check:
            if word in self.loc_title.lower():
                self.valid = True
                break
        
        if self.valid:
            # Hover over play button
            element = self.driver.find_element(By.XPATH, "/html/body/ytmusic-app/ytmusic-app-layout/div[3]/ytmusic-search-page/ytmusic-section-list-renderer/div[2]/ytmusic-shelf-renderer[1]/div[1]/ytmusic-responsive-list-item-renderer[1]/div[1]/ytmusic-thumbnail-renderer")
            hover = ActionChains(self.driver).move_to_element(element)
            hover.perform()
            time.sleep(0.5)

            # Click play button to nav to song page
            play = self.driver.find_element(By.XPATH, "/html/body/ytmusic-app/ytmusic-app-layout/div[3]/ytmusic-search-page/ytmusic-section-list-renderer/div[2]/ytmusic-shelf-renderer[1]/div[1]/ytmusic-responsive-list-item-renderer[1]/div[1]/ytmusic-item-thumbnail-overlay-renderer/div/ytmusic-play-button-renderer/div/yt-icon")
            play.click()
            time.sleep(0.75)

            # Retrieve url
            url = self.driver.current_url
            img_segment = url.split("&")[0].split("=")[1]

            # Locate artist and album
            self.loc_artist = self.driver.find_element(By.XPATH, "/html/body/ytmusic-app/ytmusic-app-layout/ytmusic-player-bar/div[2]/div[1]/span/span[2]/yt-formatted-string/a[1]").text
            self.loc_album = self.driver.find_element(By.XPATH, "/html/body/ytmusic-app/ytmusic-app-layout/ytmusic-player-bar/div[2]/div[1]/span/span[2]/yt-formatted-string/a[2]").text

            # Download cover from source then attach
            try: # sometimes thumbnail is unavailable
                src_cover = f"https://i.ytimg.com/vi/{img_segment}/maxresdefault.jpg"
                self.download(src_cover, f"covers/{self.loc_album[:15]}.jpg")
            except:
                src_cover = f"https://i.ytimg.com/vi/{img_segment}/hqdefault.jpg"
                self.download(src_cover, f"covers/{self.loc_album[:15]}.jpg")
                
            self.loc_cover = f"covers/{self.loc_album[:15]}.jpg" 
        else:
            print(unidecode.unidecode(" ".join(valid_check)) + " is not found.\n")

        time.sleep(1.5)

    # Download img while bypassing http forbidden response (403) using user-agent
    def download(self, src, loc):
        opener = urllib.request.build_opener() 
        opener.addheaders = [('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
        urllib.request.install_opener(opener)
        urllib.request.urlretrieve(src, loc)

        # if song

        # Open image and set points for cropped image 
        im = Image.open(loc) 
        width, height = im.size 
        left = (width - height) / 2
        top = 0
        right = width - left
        bottom = height

        # Cropped image of above dimension 
        im.crop((left, top, right, bottom)).save(loc)

    def get_lyrics(self):
        self.driver.switch_to.window(self.driver.window_handles[1])
        
        # Find search box and search for song
        search = self.driver.find_element_by_name('q')
        search.clear()
        search.send_keys(f"lyrics {self.loc_title} {self.loc_artist}")
        search.send_keys(Keys.RETURN)
        time.sleep(1)

        # Try to locate and expand lyrics 
        try:
            more = self.driver.find_element(By.CLASS_NAME, "vk_ard")
            more.click()
            time.sleep(0.75)

            texts = []
            for i in self.driver.find_elements(By.CSS_SELECTOR, 'div[jsname="U8S5sf"]'):
                for elem in i.find_elements(By.CSS_SELECTOR, 'span[jsname="YS01Ge"]'): 
                    if elem.text: # sometimes there are empty div
                        texts.append(f"{elem.text}\n")
                texts.append("\n")

            self.loc_lyrics = "".join(texts).replace("\n\n\n", "\n\n") # remove any double line break
        except:
            self.loc_lyrics = ""

    def finalize(self):
        # Apply changes to files
        cover = open(f"covers/{self.loc_album[:15]}.jpg", 'rb').read()
        id3 = ID3(f'review/{self.fname}')
        id3.add(APIC(3, 'image/jpeg', 3, "", cover))
        id3.add(TT2(encoding=3, text=f"{self.loc_title}"))
        id3.add(TPE1(encoding=3, text=f"{self.loc_artist}"))
        id3.add(TALB(encoding=3, text=f"{self.loc_album}"))
        id3.add(USLT(encoding=3, text=f"{self.loc_lyrics}"))

        # Save data and relocate
        id3.save(v2_version=3)
        shutil.move(f"review/{self.fname}", f"final/{self.loc_title}.mp3")   

if __name__ == "__main__":
#     from tqdm import tqdm
#     clean.GetJson(folder="review/")

    ctime = time.time()
    Finalize("songs.json")
    print(f"Thread time: {time.time() - ctime:.2f}.") # 40s

    # time.sleep(5)

    # thread1 = ReMuse(1, "Running song1.json", 0)
    # thread2 = ReMuse(2, "Running song2.json", 0)

    # ctime = time.time()
    # thread1.start()
    # thread2.start()
    # thread1.join()
    # thread2.join()
    # print(f"With threading: {time.time() - ctime:.2f}.") # 30s


    # # Run Search.py
    # with open('songs.json') as infile:
    #     songs = json.load(infile)

    # # for song in songs:
    # #     Search(song).do_something()

    # for i in tqdm(songs):
    #     for song in songs:
    #         Search(song).do_something()
 

            # print(f"File: {unidecode.unidecode(self.fname)}")
            # print(f"Artist: {unidecode.unidecode(self.loc_artist)}")
            # print(f"Title: {unidecode.unidecode(self.loc_title)}")
            # print(f"Album: {unidecode.unidecode(self.loc_album)}")
            # print(f"Lyrics: {bool(self.loc_lyrics)} >> {unidecode.unidecode(self.loc_lyrics[:20])}")
            # print(f"Cover: {bool(self.loc_cover)}")
            # print("==============================")

        # print(f"Updating... \"{unidecode.unidecode(self.fname)}\"")
        # print(f"Word: {unidecode.unidecode(word)} / Title: {unidecode.unidecode(loc_title)}.\n"
        #       f"This is the right song.\n")
