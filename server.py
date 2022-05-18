# import all modules
import json
import os
import re
import socket
import lyricsgenius

# permanent variables

albums = {}
IP = ''
PORT = 1997
ARTIST = "Pink-Floyd"
DATABASE = os.path.abspath(os.curdir) + r"\albums.json"


# save pink floyd albums in 'json' format

def update_album(Dict):  # that function add and update songs from the database using Genius API
    genius = lyricsgenius.Genius(
        "nLWcl1qMh-8SBuBG21ow_M-fsTcvSdgHjLYY0_vRmYhIjir0O-1Vyp09klBiuFfJ")  # token to access the site Genius site
    albums = genius.artist_albums(694, 50)['albums']
    regex = r"\[[^\[\]]*\]"  # format
    for i in albums:
        album_name = i['name']
        Dict.update({album_name: {}})
        specific = genius.search_album(album_name)
        for song in specific.to_dict()['tracks']:
            song_name = song['song']['title']
            lyrics = re.sub(regex, '', song['song']['lyrics'].strip())  # to list
            counter = len(lyrics.split())
            Dict[album_name].update({song_name: (lyrics, counter)})
        print(album_name, "Album updated ;-)")
    with open('albums.json', 'w') as json_file:
        json.dump(Dict, json_file)
    print("The Database is now updated!!!")


def get_albums_names(Dict):  # get all the names of albums
    string = "All Pink Floyd albums: \n"
    counter = 1
    for album_name in Dict.keys():
        if counter <= 9:
            string += "0" + str(counter) + ". " + album_name + "\n"
        else:
            string += str(counter) + ". " + album_name + "\n"
        counter += 1
    return string


def get_albums_songs(Dict, album):  # get all songs in specific album
    counter = 1
    album_name = Dict.keys()
    for title in album_name:
        if album in title:
            album_name = title
            break
    if not isinstance(album_name, str):
        return "The album not exist, please enter correct album name"
    string = "album songs list: '" + album_name + "': \n"
    for song_name in Dict[album_name].keys():
        if counter <= 9:
            string += "0" + str(counter) + ": " + song_name + "\n"
        else:
            string += str(counter) + ": " + song_name + "\n"
        counter += 1
    return string


def find_song_by_word(Dict, word):  # find a song by one word or part of the word
    name = Dict.items()
    # counter = None
    check = True
    for album_name, title in name:
        for song_name, lyrics in title.items():
            if word in lyrics[0]:
                name = song_name
                # counter = album_name
                check = False
                break
        if not check:
            break
    if not isinstance(name, str):
        return "The song not exist, please enter correct song name"
    string = "The name of the Song  is: '" + name + "'"
    return string


def running_the_server():  # start the server
    while True:
        response = "Bad Request"
        listening_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (IP, PORT)
        try:
            listening_sock.bind(server_address)
            listening_sock.listen(1)
            client_soc, client_address = listening_sock.accept()
            print("connection is open ", client_address)
            while True:  # check the phrase and checksum
                client_msg = json.loads(client_soc.recv(1024).decode())
                if client_msg[0] == "gloa" and client_msg[2] == "go419la213":
                    response = get_albums_names(albums)
                elif client_msg[0] == "fial" and client_msg[2] == "fa412il210":
                    response = get_albums_songs(albums, client_msg[1])
                elif client_msg[0] == "sole" and client_msg[2] == "sl435oe221":
                    response = get_song_length(albums, client_msg[1])
                elif client_msg[0] == "fabs" and client_msg[2] == "fb412as210":
                    response = find_album(albums, client_msg[1])
                elif client_msg[0] == "fiwo" and client_msg[2] == "fw437io222":
                    response = find_song_by_word(albums, client_msg[1])
                elif client_msg[0] == "exit" and client_msg[2] == "ei442xt225":
                    response = "Connection Closed."
                    print("connection is closed with ", client_address)
                    client_soc.sendall(response.encode())
                    break
                client_soc.sendall(response.encode())
        except ConnectionResetError:
            print("connection ended by the user -> ", client_address)

        client_soc.close()
        listening_sock.close()


def get_song_length(Dict, song):  # check how much words in specific song
    album_name = Dict.values()
    counter = None
    check = True
    name = ""
    for title in album_name:
        for song_name, lyrics in title.items():
            if song in song_name:
                name = song_name
                counter = lyrics[1]
                check = False
                break
        if not check:
            break
    if not isinstance(song_name, str) or name == "":
        return "The song not exist, please enter correct song name"
    string = "In the song: '" + name + "' have " + str(counter) + " Words"
    return string


def find_album(Dict, song):  # find album name of specific song
    name = Dict.items()
    find_album_name = None
    check = True
    for album_name, title in name:
        for song_name, lyrics in title.items():
            if song in song_name:
                name = song_name
                find_album_name = album_name
                check = False
                break
        if not check:
            break
    if not isinstance(name, str):
        return "The song not exist, please enter correct song name"
    string = "The album of the song '" + name + "' is: " + find_album_name
    return string


def load_database(al):
    with open(DATABASE) as json_file:
        al.update(json.load(json_file))
        print(
            "Database Loaded Successfully!\n\n-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_\n-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_\n-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_")


if os.path.isfile(DATABASE):
    print("database exist\nDo you want to update database? (Y/N)")
    answer = input().upper()
    if answer == 'Y':
        update_album(albums)
    elif answer == 'N':
        print("database don't updated")
        load_database(albums)
    else:
        print("Wrong input,continue with the existing database")
        load_database(albums)
else:
    print("updating Database\n************************************************************")
    update_album(albums)
running_the_server()
