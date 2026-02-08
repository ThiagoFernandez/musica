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
import shutil
import time
import mutagen
from mutagen.mp3 import MP3

def download_music(playlist):
    while True:
        try:
            option = int(input(f"1 -> song\n2 -> playlist\n3 -> exit\nChoose an option: "))
            if option == 3:
                return None
            else:
                if option < 1 or option > 3:
                    print("The option must be between 1-3 | Try again")
                else:
                    if option == 1:
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
                    else:
                        url = input(
                            "Copy the link from youtube\n"
                            "To paste use 'ctrl + shift + v'\n>>>: "
                        ).strip()

                        output_path = os.path.join(LIBRARY_DIR, playlist, "%(title)s.%(ext)s")

                        subprocess.run([
                            sys.executable,
                            "-m", "yt_dlp",
                            "-x",
                            "--audio-format", "mp3",
                            "--audio-quality", "0",
                            "-o", output_path,
                            url
                        ])
        except ValueError:
            print("The option must be a number | Try again")

def create_playlist():
    new_playlist = input("Write the name of your new playlist: ").strip()
    playlist_path = os.path.join(LIBRARY_DIR, new_playlist)

    if os.path.exists(playlist_path):
        print(f"The playlist - {new_playlist} already exists")
    else:
        os.mkdir(playlist_path)
        print(f"The playlist - {new_playlist} was created")
    return None


def song_controller_input():
    print("\n[P]ause | [R]esume | [U] Vol+ | [D] Vol- | [N]ext | [S]top")
    option = input(">>> ").strip().upper()

    step = 0.1

    match option:
        case "P":
            pygame.mixer.music.pause()
        case "R":
            pygame.mixer.music.unpause()
        case "U":
            vol = pygame.mixer.music.get_volume()
            pygame.mixer.music.set_volume(min(1.0, vol + step))
        case "D":
            vol = pygame.mixer.music.get_volume()
            pygame.mixer.music.set_volume(max(0.0, vol - step))
        case "N":
            pygame.mixer.music.stop()
            return 1
        case "S":
            pygame.mixer.music.stop()
            return -1

    return 0



def play_song(song_path):
    print(f"\n▶ Reproduciendo: {os.path.basename(song_path)}")

    pygame.mixer.music.load(song_path)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        state = song_controller_input()

        if state == -1:
            return -1   
        elif state == 1:
            return 1   

    return 0  


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
                random.shuffle(songs)

                for song in songs:
                    song_path = os.path.join(playlist_path, song)
                    state = play_song(song_path)
                    if state == -1:
                        return None
                    elif state == 1:
                        print("Skipping song...")
                        continue
            else:
                for song in all_songs:
                    song_path = os.path.join(playlist_path, song)
                    state = play_song(song_path)
                    if state == -1:
                        return None
                    elif state == 1:
                        print("Skipping song...")
                        continue
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

def delete_playlist():
    playlist = pick_playlist()
    if playlist != None:
        path = os.path.join(LIBRARY_DIR, playlist)
        try:
            shutil.rmtree(path)
            print(f"Directory '{path}' and all its contents deleted successfully.")
        except FileNotFoundError:
            print(f"Directory '{path}' not found.")
        except Exception as e:
            print(f"Error deleting directory: {e}")
    return None

def delete_song():
    playlist = pick_playlist()
    if playlist != None:
        playlist_path = os.path.join(LIBRARY_DIR, playlist)
        all_songs = os.listdir(playlist_path)
        for i, song in enumerate(all_songs):
            print(f"{i+1}. {song}")
        print(f"{len(all_songs)+1}. Exit")
        while True:
            try:
                option = int(input("Choose an option: "))
                if option == len(all_songs)+1:
                    return None
                else:
                    song_path = os.path.join(playlist_path, all_songs[option-1])
                    os.remove(song_path)
                    return None
            except ValueError:
                print("The option must be a number | Try again")

def delete_what():
    while True:
        print(f"1 -> Song\n2 -> Playlist\n3 ->Exit")
        try:
            option = int(input("Choose an option: "))
            if option == 3:
                return None
            else:
                if option < 1 or option > 3:
                    print("The option must be between 1-3 | Try again")
                else:
                    if option == 1:
                        delete_song()
                        return None
                    else:
                        delete_playlist()
                        return None
        except ValueError:
            print("The option must be a number | Try again")

def change_directory():
    playlist = pick_playlist()
    if playlist != None:
        playlist_path = os.path.join(LIBRARY_DIR, playlist)
        all_songs = os.listdir(playlist_path)
        for i, song in enumerate(all_songs):
            print(f"{i+1}. {song}")
        print(f"{len(all_songs)+1}. Exit")
        while True:
            try:
                option = int(input("Choose an option: "))
                if option == len(all_songs)+1:
                    return None
                else:
                    song_path = os.path.join(playlist_path, all_songs[option-1])
                    song = all_songs[option-1]
                    new_playlist= pick_playlist()
                    new_dir = os.path.join(LIBRARY_DIR, new_playlist, song)
                    if new_dir != None:
                        try:
                            shutil.copyfile(song_path, new_dir)
                            print(f"File '{song_path}' copied to '{new_dir}' successfully.")
                            os.remove(song_path)
                        except shutil.SameFileError:
                            print("Source and destination represent the same file.")
                        except PermissionError:
                            print("Permission denied.")
                        except FileNotFoundError:
                            print("Source file not found.")
                        except Exception as e:
                            print(f"An error occurred: {e}")
                    return None
            except ValueError:
                print("The option must be a number | Try again")
        

def main_menu():
    while True:
        print(f"{'Welcome to the jambot':-^60}\n1. Pick a playlist\n2. Create a playlist\n3. Delete a playlist/song\n4. Download a song/playlist\n5. Change song's playlist\n6. Exit")
        while True:
            try:
                option = int(input("Choose an option: "))
                if option < 1 or option >7:
                    print("The option must be between 1-6 | Try again")
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
                delete_what()
            case 4:
                print("--Which playlist")
                playlist = pick_playlist()
                if playlist != None:
                    download_music(playlist)
            case 5:
                change_directory()
                pass
            case 6:
                break

#m.p
BASE_DIR = "/home/zanto/Desktop/musica"
LIBRARY_DIR = os.path.join(BASE_DIR, "library")
if not os.path.exists(LIBRARY_DIR):
    os.mkdir(LIBRARY_DIR)
pygame.mixer.init()
pygame.mixer.music.set_volume(0.5) # tambien puede llegar a estar en un file de settings
SONG_END = pygame.USEREVENT + 1
pygame.mixer.music.set_endevent(SONG_END)
main_menu()

