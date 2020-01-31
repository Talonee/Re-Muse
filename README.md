Re-Muse is an app that takes in a music file's name and attempt to fill in any missing metadata such as album, cover art and lyrics. 

# TO DO:

- Generalize all input and out sources
    -     `print(os.path.dirname(os.path.abspath(__file__)))`


## Flow
1. Navigate to Youtube music for title/artist/cover/album, Google for lyrics
2. If no artist (no dash), mark for review
3. Attempt search for 'Song,' get TACA, crop cover
4. Attempt search for 'Video,' get TACA, crop cover. Mark for review

# Future
1. Download mp3



## Clean and GetJson (clean.py)

1. Find pre-existing data and initiate attributes. ✓
2. Compile into Json and export (fname, artist, title, album, lyrics). ✓


## Class 2 (Search) (try, except simulator) 

1. Search artist, title, album, cover, lyrics. ✓
2. Create database for albums and artists.
3. Exception cases for videos and non-existing song.
4. Save metadata and finalize modification. ✓

## Class 3 (App)

1. Welcome message.
2. Browse folder to clean and search.
3. Show live update (tqdb).
4. Review: Show lists of songs in need of review
5. Prompt for manual input of artist information

- Optional: Access phone subfolders, pull and modify songs




## Useful links to references

https://stackoverflow.com/questions/42665036/python-mutagen-add-image-cover-doesnt-work

https://stackoverflow.com/questions/18026516/how-to-set-artist-album-artist-year-album-song-number-and-title?rq=1

http://ws.audioscrobbler.com/2.0/?method=album.getinfo&api_key=abfef408b828ff61598e0f0d2ce83dcc&artist=bich%20phuong&album=Dramatic&format=json

https://riptutorial.com/pyqt5/example/29500/basic-pyqt-progress-bar