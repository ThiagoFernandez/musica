#!/usr/bin/env python3
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)
warnings.filterwarnings("ignore", category=UserWarning)
import subprocess
import sys
import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame
import random

def download_music(playlist):
    url = input(
        "Copy the link from youtube\n"
        "To paste use 'ctrl + shift + v'\n>>>: "
    ).strip()

    output_path = os.path.join(LIBRARY_DIR, playlist, "%(title)s.%(ext)s")

    subprocess.run([
        sys.executable,
        "-m", "yt_dlp",
        "--no-playlist", # para el file settings lo mas probable
        "-x",
        "--audio-format", "mp3",
        "--audio-quality", "0",
        "-o", output_path,
        url
    ])

def create_playlist():
    new_playlist = input("Write the name of your new playlist: ").strip()
    playlist_path = os.path.join(LIBRARY_DIR, new_playlist)

    if os.path.exists(playlist_path):
        print(f"The playlist - {new_playlist} already exists")
    else:
        os.mkdir(playlist_path)
        print(f"The playlist - {new_playlist} was created")
    return None

def song_controller_input_light():
    step = 0.1
    playing = True

    print("\n[P]ause | [R]esume | [S]top | [U]p vol | [D]own vol | [E]xit")

    while playing:
        option = input(">>> ").strip().upper()

        match option:
            case "P":
                pygame.mixer.music.pause()

            case "R":
                pygame.mixer.music.unpause()

            case "S":
                pygame.mixer.music.stop()
                playing = False 
                return None

            case "U":
                vol = pygame.mixer.music.get_volume()
                pygame.mixer.music.set_volume(min(1.0, vol + step))
                print(f"Volume: {pygame.mixer.music.get_volume():.1f}")

            case "D":
                vol = pygame.mixer.music.get_volume()
                pygame.mixer.music.set_volume(max(0.0, vol - step))
                print(f"Volume: {pygame.mixer.music.get_volume():.1f}")

            case "E":
                return  None

            case _:
                print("Invalid command")    

def song_controller_input():
    step = 0.1
    playing = True

    print("\n[P]ause | [R]esume | [S]top | [U]p vol | [D]own vol | [N]ext | [E]xit")

    while playing:
        option = input(">>> ").strip().upper()

        match option:
            case "P":
                pygame.mixer.music.pause()

            case "R":
                pygame.mixer.music.unpause()

            case "S":
                pygame.mixer.music.stop()
                playing = False 
                return -1

            case "U":
                vol = pygame.mixer.music.get_volume()
                pygame.mixer.music.set_volume(min(1.0, vol + step))
                print(f"Volume: {pygame.mixer.music.get_volume():.1f}")

            case "D":
                vol = pygame.mixer.music.get_volume()
                pygame.mixer.music.set_volume(max(0.0, vol - step))
                print(f"Volume: {pygame.mixer.music.get_volume():.1f}")

            case "E":
                return -1
            
            case "N":
                return 1

            case _:
                print("Invalid command")



def play_song(song_path):
    pygame.mixer.music.load(song_path)
    pygame.mixer.music.play()

    state = song_controller_input()
    if state == -1:
        return -1
    else:
        return None

# modificar para que sea global y no solo una playlist
# def pick_song(playlist):
#     all_songs = os.listdir(f"/home/zanto/Desktop/musica/library/{playlist}")
#     if len(all_songs) == 0:
#         print(f"Songs found = 0\nBack to the menu")
#         return None
#     else:
#         while True:
#             for idx, song in enumerate(all_songs):
#                 print(f"{i+1}. {song}")
#             print(f"{len(all_songs)+1}. Exit")
#             try:
#                 option = int(input("Choose an option: "))
#                 if option == len(all_songs)+1:
#                     print("Back to the menu")
#                     return None
#                 else:
#                     if option < 1 or option > len(all_songs):
#                         song_path = os.path.join("library", playlist, all_songs[option-1])
#                         play_song(song_path)
#             except ValueError:
#                 print("The option must be a number | Try again")

def play_playlist(playlist):
    playlist_path = os.path.join(LIBRARY_DIR, playlist)
    all_songs = os.listdir(playlist_path)

    if not all_songs:
        print("Playlist empty\nBack to the menu")
        return

    while True:
        print("Shuffle mode")  # posible agregado a un file de settings futuro
        print("1. Shuffle on")
        print("2. Shuffle off")
        print("3. Exit")

        try:
            option = int(input("Choose an option: "))

            if option == 3:
                print("Back to the menu")
                return None

            if option < 1 or option > 3:
                print("The option must be between 1-3 | Try again")
                continue

            if option == 1:
                songs = all_songs.copy()
                while songs:
                    song = random.choice(songs)
                    songs.remove(song)
                    song_path = os.path.join(playlist_path, song)
                    state = play_song(song_path)
                    if state== -1:
                        return None

            else:
                for song in all_songs:
                    song_path = os.path.join(playlist_path, song)
                    state = play_song(song_path)
                    if state == -1:
                        return None

        except ValueError:
            print("The option must be a number | Try again")

def pick_playlist():
    all_playlists = os.listdir(LIBRARY_DIR)
    if len(all_playlists) == 0:
        print(f"Playlist found = 0\nBack to the menu")
        return None
    else:
        while True:
            for idx, playlist in enumerate(all_playlists):
                print(f"{idx+1}. {playlist}")
            print(f"{len(all_playlists)+1}. Exit")
            try:
                option = int(input("Choose an option: "))
                if option == len(all_playlists)+1:
                    print("Back to the menu")
                    return None
                else:
                    if option < 1 or option > len(all_playlists):
                        print(f"The option must be between 1-{len(playlist)}")
                    else:
                        return all_playlists[option-1]
                        
            except ValueError:
                print("The option must be a number | Try again")


#m.p
BASE_DIR = "/home/zanto/Desktop/musica"
LIBRARY_DIR = os.path.join(BASE_DIR, "library")
if not os.path.exists(LIBRARY_DIR):
    os.mkdir(LIBRARY_DIR)
pygame.mixer.init()
pygame.mixer.music.set_volume(0.5) # tambien puede llegar a estar en un file de settings
SONG_END = pygame.USEREVENT + 1
pygame.mixer.music.set_endevent(SONG_END)

while True:
    print(f"{'Welcome to the jambot':-^60}\n1. Pick a playlist\n2. Create a playlist\n3. Delete a playlist\n4. Download a song\n5. Change song's playlist\n6. Music controller\n7. Exit")
    while True:
        try:
            option = int(input("Choose an option: "))
            if option < 1 or option >7:
                print("The option must be between 1-7 | Try again")
            else:
                break
        except ValueError:
            print("The option must be a number | Try again")
    match option:
        case 1:
            playlist = pick_playlist()
            if playlist != None:
                play_playlist(playlist)
        case 2:
            create_playlist()
        case 3:
            pass
        case 4:
            print("--Which playlist")
            playlist = pick_playlist()
            if playlist != None:
                download_music(playlist)
        case 5:
            pass
        case 6:
            song_controller_input_light() # temporal el light, la idea es poder skippear dsd aca pero tengo que buscar como
        case 7:
            break