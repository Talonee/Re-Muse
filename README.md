Re-Muse is an app that takes in a music file's name and attempt to fill in any missing metadata such as album, cover art and lyrics. 

# TO DO:

## Class 1 (Clean)

1. Initiate all relevant attributes to default.
2. Find pre-existing data, change initial attributes if applicable.
3. Compile into Json and export (fname, artist, title, album, lyrics).
4. Rename files.

## Class 2 (Search) (try, except simulator) 

1. **Search_lyrics**

    > Lyrics
    1. `Try:`
        * Locate lyrics
    2. `Except:` >> No artist/title.
        1. `Try:`
            * Split artist + title if applicable.
        2. `Except:`
            * Pass.

2. **Search_alb_cov**

    > Album + Cover
    1. `If album not in album_stor:`
        1. `If (artist and title) or (title and album):`
            1. `Try:` *(Search album)* 
                * Locate album. `f"{album artist title album}`

                1. `If not artist:`
                    1. `Try:`
                        * Artist = `f"{artist title album}`
                    2. `Except:`
                        * Artist = ""

                1. `If album`:
                    * Add to album_stor
                    1. `Try:` *(Search cover)*
                        * Locate cover art.
                    2. `Except:` *(No cover)*
                        1. `If artist:`
                            1. `Try:` *(Search cover)*
                                * Search cover with url.parsed artist and album (last.fm).
                            2. `Except:` *(No result)*
                                1. `Try:` *(Search cover)*
                                    * Flip artist + album in API url for possible result.
                                2. `Except:` *(No result)*
                                    * `Pass.`
                2. `Else:`    
                    * Set album to title.
                    1. `Try:` *(Search cover)*
                        * Search cover with url.parsed artist and title (last.fm).
                    2. `Except:` *(No result)*
                        1. `Try:` *(Search cover)*
                            * Flip artist + title in API url for possible result.
                        2. `Except:` *(No result)*
                            * `Pass.`
            2. Except: *(No album)*
                * `Pass.`

    1. `If album == "":` 
        1. `If (artist and title):`
            1. `Try:` *(Search album)* 
                * Locate album. `f"{album artist title}`
            2. Except: *(No album)*
                * `Pass.`
    2. `Elif album and album not in album_stor:`
        1. `If (title and album):`
            1. `Try:` *(Search album)* 
                * Locate album. `f"{album artist title album}`


**Any violation goes to the Review folder.**

2. **Cover Resize**
    1. `If cover:`
        1. `Try:` *(GRIS)*
            * GRIS.
            * Retrieve larger cover.

## Ad to existing album

3. **Update** artist, title, lyrics, album

3. Check for cover art
- Get HD cover art + resize (store those of smaller sizes) (800-1500px)
    - If below 800, store and manually edit
    + Try extract the associated album cover result
        + Except: retrieve from last.fm
        + Finally: GRIS the result
- Database for artists
- Only put title for file name
- Find a way to check for preexisting meta data

### Class 3 (App)
- Create a Kivy app that shows live update (tqdb, too?)
- Asks for artist information

- Optional: Access phone subfolders, pull and modify songs