import requests
import math

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
user_ID = '316czvcyfahvkhleblryjlnep6ai'
#user_ID = current_user_info['id']

# get user playlists
user_playlists_info = requests.get(BASE_URL + 'users/' + user_ID + '/playlists', headers=headers).json()
number_of_playlists = user_playlists_info['total']

print(user_playlists_info) # debugging

for i in user_playlists_info['items']: # for each playlist
    output_file.write('playlist: ' + i['name'] + '\n') # write playlist name to file
    total_playlist_length = 0
    most_popular_song = [] # list of most popular songs in playlist
    song_popularity = 0 # popularity of most popular song
    # make a call using href to get playlist info
    single_playlist_info = requests.get(i['tracks']['href'], headers=headers).json()
    # for each playlist, get all tracks and determine their average length
    for j in single_playlist_info['items']: # for each track in playlist
        total_playlist_length += j['track']['duration_ms'] # get track length in ms
        if j['track']['popularity'] > song_popularity or song_popularity:
            most_popular_song.clear() # clear list of most popular songs
            most_popular_song = [j['track']['name']] # add song to list of most popular songs
            song_popularity = j['track']['popularity'] # set song popularity to current song's popularity
        elif j['track']['popularity'] == song_popularity:
            most_popular_song.append(j['track']['name']) # add song to list of most popular songs
        
    average_playlist_length = round(((total_playlist_length/1000) / single_playlist_info['total'])/60, 2) # get average length in minutes
    out = math.modf(average_playlist_length)
    output_file.write('average length: ' + str(round(out[1], 1)) + ' minutes and ' + str(round(out[0] * 60, 2)) + ' seconds' + '\n') # write average length to file
    output_file.write('most popular song(s): ' + str(most_popular_song) + '\n\n') # write most popular song(s) to file
    
output_file.close()