import requests
from dataclasses import dataclass

def getRandomSongName(songsInPlaylist, allSongNames):
    import random
    randomSongIndex = random.randint(0, songsInPlaylist - 1)
    return allSongNames[randomSongIndex]

@dataclass
class Information:
    playlist_name: str
    songsInPlaylist: float
    allSongNames = []   

# Client Keys
CLIENT_ID = 'yourclientid'
CLIENT_ID = 'a8fbe860846c4c05ac7acce925209c3a'
CLIENT_SECRET = 'yourclientsecret'
CLIENT_SECRET = '3bd1d0e8d1ab4adb8c3614079d4dc19b'

AUTH_URL = 'https://accounts.spotify.com/api/token'

# base URL of all Spotify API endpoints
BASE_URL = 'https://api.spotify.com/v1/'

# POST
auth_response_data = requests.post(AUTH_URL, {
    'grant_type': 'client_credentials',
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
}).json()

# save the access token
access_token = auth_response_data['access_token']

headers = {
    'Authorization': 'Bearer {token}'.format(token=access_token)
}

#user_ID = '316czvcyfahvkhleblryjlnep6ai' # mine
user_ID = 'mylesstyles' # milly

# declare class to store playlist info
playlist_dict = {}

# get user playlists
user_playlists_info = requests.get(BASE_URL + 'users/' + user_ID + '/playlists?offset=0&limit=1', headers=headers).json()

while user_playlists_info: # while there are more playlists to get (has 1 playlist per call)
    new_playlist_info = Information(user_playlists_info['items'][0]['name'], 0) # create new playlist info object
    allSongNames = [] # create new list to store all song names in current playlist
    single_playlist_info = requests.get(user_playlists_info['items'][0]['tracks']['href'], headers=headers).json()
    # for each playlist, get all tracks and determine their average length
        
    while single_playlist_info: # while there are more tracks to get
        for i in single_playlist_info['items']: # for each track in the playlist (has 100 tracks per call)
            allSongNames.append(i['track']['name']) # add song name to list
        if single_playlist_info['next'] == None:
                break
        single_playlist_info = requests.get(single_playlist_info['next'], headers=headers).json() # get next batch of tracks
            
    new_playlist_info.songsInPlaylist = len(allSongNames) # set number of songs in playlist
    new_playlist_info.allSongNames = allSongNames # set list of all song names in playlist
    new_playlist_info.playlist_name = user_playlists_info['items'][0]['name'] # set playlist name
    
    playlist_dict[new_playlist_info.playlist_name] = new_playlist_info # add playlist info to dict
                
    if user_playlists_info['next'] == None:
        break
    user_playlists_info = requests.get(user_playlists_info['next'], headers=headers).json() # get next batch of playlists
    

# now a dict of key of playlist names and values of classes for info exists of all playlists and their songs

# get random song name from playlist
randomSongName = getRandomSongName(playlist_dict['Chillin and Killin'].songsInPlaylist, playlist_dict['Chillin and Killin'].allSongNames)
print(randomSongName)