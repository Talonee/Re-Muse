from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, TT2, TPE1, TRCK, TALB, USLT, error
# ID3 info:
# APIC: picture
# TT2: title
# TPE1: artist
# TRCK: track number
# TALB: album
# USLT: lyric

pic_file = 'test/cat.jpg' # pic file
imagedata = open(pic_file, 'rb').read()

id3 = ID3('test/Clueless.mp3')
id3.add(APIC(3, 'image/jpeg', 3, 'Front cover', imagedata))
id3.add(TT2(encoding=3, text='title'))

id3.save(v2_version=3)
