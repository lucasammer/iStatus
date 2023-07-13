import win32com.client
import pypresence
import requests
import time
import psutil
from datetime import datetime, timedelta

# Connect to iTunes COM interface
itunes = win32com.client.Dispatch('iTunes.Application')

# Initialize the song cache
songCache = {}

# Display song details on Discord
client_id = '1106665848346775623'
RPC = pypresence.Presence(client_id=client_id)
RPC.connect()

interval = 1

playing = ""
foundDate = datetime(1,1,1)

while True:
    while not "Discord.exe" in (p.name() for p in psutil.process_iter()) and not "DiscordCanary.exe" in (p.name() for p in psutil.process_iter()) and not "DiscordPTB.exe" in (p.name() for p in psutil.process_iter()):
        time.sleep(1)

    try:
        # Get the current playing track
        track = itunes.CurrentTrack

        # print(track.Time) # duration in mm:ss
        # print(track.Duration) # duration in s

        location = (datetime.now() - foundDate).total_seconds()
        minutes, seconds = divmod(location, 60)
        if((int(location // 7) % 2) == 0):
            toshow = 0
        else:
            toshow = 1

        # If there's nothing playing show thats
        if(track == None):
            RPC.update(details="not playing", state="not playing", large_image="https://hips.hearstapps.com/hmg-prod.s3.amazonaws.com/images/ez49erpwqae5b-a-1619449002.jpeg?resize=480:*")
            continue

        # Extract song details
        song_name = track.Name
        artist_name = track.Artist
        album_name = track.Album

        # If the song is not yet cached cache it else get it using the itunes api
        if(songCache.keys().__contains__(song_name + artist_name + album_name)):
            results = songCache.get(song_name + artist_name + album_name)
        else:
            url = ("https://itunes.apple.com/search?term=" + song_name + " by " + artist_name + " " + album_name)

            response = requests.get(url)
            results = response.json()
            songCache[song_name + artist_name + album_name] = results

        # If the song is not the same as in playing then change it and the found date
        if(song_name != playing):
            playing = song_name
            foundDate = datetime.now()

        # Get the album cover and url's to song from the request or cache
        album_cover_url = results["results"][0]["artworkUrl100"].replace("100x100bb", "1000x1000bb")
        button = {"label": "view album", "url": results["results"][0]["collectionViewUrl"]}
        button1 = {"label": "view song", "url": results["results"][0]["trackViewUrl"]}

        # What is currently being shown
        if(toshow == 0):
            showing = "by: " + artist_name + " | " + album_name
            title = song_name
        else:
            showing = "{:02d}:{:02d} - {}".format(int(minutes), round(seconds), track.Time)
            title = song_name + " - " + artist_name

        # Update Presence
        RPC.update(details=title, state=showing, large_image=album_cover_url, buttons=[button,button1])
    except Exception as e:
        print(e)
        # If there is an error, blame the user for not having itunes opened
        RPC.update(details="no itunes", state="itunes not opened :(", large_image="https://static.wikia.nocookie.net/0e9418e5-bf6c-4353-8702-5b7ec0b56a52/scale-to-width/755")
        while True:
            # Wait for itunes to be opened
            if "iTunes.exe" in (p.name() for p in psutil.process_iter()):
                break
            time.sleep(1)
        # Reconnect to itunes
        itunes = win32com.client.Dispatch('iTunes.Application')
    sleep(interval)