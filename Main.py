import requests
import math
from dataclasses import dataclass

@dataclass
class Information:
    name: str
    playlist_length: float
    most_popular_song: str

# make a text file for output
output_file = open('output.txt', 'w')

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

# get user ID
current_user_info = requests.get(BASE_URL + 'me', headers=headers).json()

print(current_user_info) # debugging

#https://open.spotify.com/user/316czvcyfahvkhleblryjlnep6ai?si=1531790de7d44fa0
#user_ID = '316czvcyfahvkhleblryjlnep6ai' # mine
#user_ID = 'hreynoldsbae' # holly
#user_ID = 'l9ctc6gi1wzxx6dxhmd8ojdtt' # dalton
#user_ID = current_user_info['id']
user_ID = 'mylesstyles' # milly

# get user playlists
user_playlists_info = requests.get(BASE_URL + 'users/' + user_ID + '/playlists?offset=0&limit=1', headers=headers).json()

output_info = [] # list of all playlist info

while user_playlists_info: # while there are more playlists to get (has 1 playlist per call)
    new_playlist_info = Information(user_playlists_info['items'][0]['name'], 0, '') # create new playlist info object
    print(user_playlists_info['items'][0]['name']) # debugging
    total_playlist_length = 0
    most_popular_song = '' # most popular song in playlist
    song_popularity = 0 # popularity of most popular song
    # make a call using href to get playlist info
    single_playlist_info = requests.get(user_playlists_info['items'][0]['tracks']['href'], headers=headers).json()
    # for each playlist, get all tracks and determine their average length
        
    while single_playlist_info: # while there are more tracks to get
        for i in single_playlist_info['items']: # for each track in the playlist (has 100 tracks per call)
            if i['track'] == None: # some old tracks have this issue
                continue
            total_playlist_length += (i['track']['duration_ms'])/1000 # get track length from ms to s
            if i['track']['popularity'] > song_popularity:
                most_popular_song = i['track']['name'] # add song to list of most popular songs
                song_popularity = i['track']['popularity'] # set song popularity to current song's popularity
        if single_playlist_info['next'] == None:
                break
        single_playlist_info = requests.get(single_playlist_info['next'], headers=headers).json() # get next batch of tracks
            
    new_playlist_info.most_popular_song = most_popular_song
    new_playlist_info.playlist_length = total_playlist_length/single_playlist_info['total']/60
    print(new_playlist_info.playlist_length) # debugging
    
    # add playlist info to list
    output_info.append(new_playlist_info)
        
    if user_playlists_info['next'] == None:
        break
    user_playlists_info = requests.get(user_playlists_info['next'], headers=headers).json() # get next batch of playlists
    
# sort list by playlist length
output_info.sort(key=lambda x: x.playlist_length, reverse=True)  
    
# write to output file
for i in output_info:
    output_file.write(i.name + '\n') # write playlist name to file
    out = math.modf(i.playlist_length)
    output_file.write('length: ' + str(round(out[1], 1)) + ' minutes and ' + str(round(out[0] * 60, 2)) + ' seconds' + '\n') # write playlist length to file
    output_file.write('most popular song: ' + str(i.most_popular_song) + '\n\n') # write most popular song to file
    
output_file.close()