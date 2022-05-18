# import all modules


import socket
import json
import time
import hashlib

# permanent variables

IP = '192.168.56.1'
PORT = 1997
BUFFER = 1024


def create_check_sum(phrase):
    calculate_checksum = str(phrase[0] + phrase[2])
    calculate_checksum += str(sum(map(ord, phrase)))
    calculate_checksum += str(phrase[1] + phrase[3])
    calculate_checksum += str(sum(map(ord, phrase)) // 2 + 4)
    return calculate_checksum


def find_album():
    checksum = create_check_sum("fial")
    print("Please enter the name of the album-->")
    ans = input()
    return tuple(("fial", ans, checksum))


def song_length():
    print("Please enter the name of the song: ")
    ans = input()
    checksum = create_check_sum("sole")
    return tuple(("sole", ans, checksum))


def find_album_by_song():
    print("Please enter the name of the song: ")
    ans = input()
    checksum = create_check_sum("fabs")
    return tuple(("fabs", ans, checksum))


def find_words():
    print("Please enter the word in the song-->")
    checksum = create_check_sum("fiwo")
    ans = input()
    return tuple(("fiwo", ans, checksum))


def main():
    while True:
        while True:
            try:
                connect = socket.socket()
                address = (IP, PORT)
                connect.connect(address)
                break
            except ConnectionRefusedError:
                print("error in connection, we try again in 3 seconds'")
                time.sleep(3)

        print("Connection Successful!")
        while True:
            print('''Please choose an option from the menu:
            1. Get the list of pink floyd albums
            2. Get songs of specific album
            3. Get song length
            4. Find album of a specific song
            5. Find song by a specific word
            6. Exit''')
            buffer = 1024
            answer = input()
            if answer == "1":
                buffer = 2048
                answer = tuple(("gloa", 0, create_check_sum("gloa")))
            elif answer == "2":
                answer = find_album()
            elif answer == "3":
                answer = song_length()
            elif answer == "4":
                answer = find_album_by_song()
            elif answer == "5":
                answer = find_words()
            elif answer == "6":
                answer = tuple(("exit", 0, create_check_sum("exit")))

            try:
                connect.sendall(json.dumps(answer).encode())
                response = connect.recv(buffer)

            except:
                print("Connection ended without except")
                break

            print(response.decode())
            if response.decode() == "Connection Closed!":
                break

        connect.close()
        print("Would you like to renew connection to the server? (Y/N)")
        answer = input().upper()
        if answer == 'Y':
            print(
                "Renewing session\n-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_\n-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_\n-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_")
        elif answer == 'N':
            print(
                "See you next Time!\nWe hope you enjoyed our services\nlook forward to seeing you again\n\nBye bye :)")
            break

        else:
            print("Wrong input, Closing app")
            break


if __name__ == '__main__':
    main()
