Re-Muse is an interactive application which browses for music files' name and attempt to fill in any missing metadata such as title, artist, album, cover art and lyrics. 

# Files:

## Clean and GetJson (`clean.py`)

1. Find pre-existing data and initiate attributes. ✓
2. Compile into Json and export (fname, artist, title, album, lyrics). ✓


## Search (`search.py`)

1. Search artist, title, album, cover, lyrics. ✓
2. Create database for albums and artists.
3. Exception cases for videos and non-existing song.
4. Save metadata and finalize modification. ✓

## Re-Muse (`main.py`)

1. Open app with a welcoming message. ✓
2. Browse folder to clean. ✓
3. Multithreading search. ✓
4. Show live update with progress bar. ✓
5. Review: Show lists of songs completed ✓
6. Review: Show lists of songs failed

# Results:

![Recording](assets/remuse_v1.gif)

*Please navigate to `assets/` for a clearer video (remuse_v1.mp4)*

## Useful links to references

https://stackoverflow.com/questions/42665036/python-mutagen-add-image-cover-doesnt-work

https://stackoverflow.com/questions/18026516/how-to-set-artist-album-artist-year-album-song-number-and-title?rq=1

http://ws.audioscrobbler.com/2.0/?method=album.getinfo&api_key=abfef408b828ff61598e0f0d2ce83dcc&artist=bich%20phuong&album=Dramatic&format=json

https://riptutorial.com/pyqt5/example/29500/basic-pyqt-progress-bar

https://www.learnpyqt.com/courses/adanced-ui-features/qscrollarea/


## Flow
1. Navigate to Youtube music for title/artist/cover/album, Google for lyrics
2. If no artist (no dash), mark for review
3. Attempt search for 'Song,' get TACA, crop cover
4. Attempt search for 'Video,' get TACA, crop cover. Mark for review

## Future
1. Download mp3
2. Manual information input
3. Optional: Access subfolders, pull and modify songs
4. Show current file mod in progress page


## Version 1 

- Browse a list of folders with song files.
- Clean, search, and modify song metadata.
- Show list of successfully completed songs.