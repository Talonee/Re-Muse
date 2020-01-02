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
        self.artist = self.fname.split("-")[0]
        try:
            self.title = self.fname.split("-")[1]
        except:
            self.title = ""

        return self.artist.strip(), self.title.strip()


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import time

class Search():
    def __init__(self):
        pass

    def open(self):
        driver = webdriver.Chrome()
        options = Options()
        # options.add_argument("headless")
        # driver = webdriver.Chrome(executable_path='chromedriver', options=options)
        
        driver.get("http://www.google.com/")
        # driver.execute_script("window.open('http://www.google.com/');")
        # driver.switch_to.window(driver.window_handles[1])
        search = driver.find_element_by_name('q')
        # search.send_keys(f"lyrics bich phuong chu meo")
        search.send_keys(f"lyrics jaden goku")
        search.send_keys(Keys.RETURN)
        time.sleep(1)

        # Run iff Mr. Google returns a valid address
        try:
            more = driver.find_element(By.CLASS_NAME, "vk_ard")
            more.click()
            for elem in driver.find_elements(By.CSS_SELECTOR, 'span[jsname="YS01Ge"]'):
                print(unidecode.unidecode(elem.text))

        #     # //*[@id="tsuid22"]/span/div/div/div[2]/div/div/div/div[1]/div[1]/div[1]/span[1]
        #     # //*[@id="tsuid22"]/span/div/div/div[2]/div/div/div/div[1]/div[1]/div[1]/span[2]
            

        #     # //*[@id="tsuid22"]/span/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/span[1]

        #     # //*[@id="tsuid22"]/span/div/div/div[2]/div/div/div/div[1]/div[2]/div[5]
        except:
            print("I choked.")


        # driver.get("https://thumbs-prod.si-cdn.com/n7Z82GD9Eav_CtpnzizNo66-dKc=/420x240/https://public-media.si-cdn.com/filer/d6/93/d6939718-4e41-44a8-a8f3-d13648d2bcd0/c3npbx.jpg")
        # driver.get_screenshot_as_file("capture.png")
        driver.close()


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

    Search().open()