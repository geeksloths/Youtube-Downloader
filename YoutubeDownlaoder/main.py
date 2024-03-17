# url: https://www.youtube.com/watch?v=B8VfZWBEsYY
import math
import os
import threading

from pytube import YouTube
from tqdm import tqdm

from byte_convertor import Convertor
from time_convertor import Time
from list_files import get as directories_get

DEFAULT_DOWNLOAD_PATH = 'Downloads'

default_folders = {
}

DOWNLOADED = 0


def get_directories():
    folders = directories_get(direction=DEFAULT_DOWNLOAD_PATH)
    if default_folders == {}:
        for folder in folders:
            folder_list(folder)


def progress_callback(stream, file_handle, bytes_remaining):
    downloaded_size = math.ceil(stream.filesize - bytes_remaining)
    global DOWNLOADED
    DOWNLOADED = downloaded_size
    percent = math.ceil((downloaded_size / stream.filesize) * 100)
    downloaded_size = Convertor(size=downloaded_size).convert()
    download_listener(filesize=stream.filesize)
    remained_size = math.ceil(bytes_remaining)
    remained_size = Convertor(size=remained_size).convert()
    # print(f"Progress: {percent}% | Remained: {remained_size} | Downloaded: {downloaded_size}")


def start():
    get_directories()
    link = input("Enter Your Link: ")
    if link == "exit":
        exit()
    yt = YouTube(url=link, on_progress_callback=progress_callback)
    get_details(yt)
    streams = yt.streams.filter(progressive=True)
    ID = get_stream(streams)
    chosen = yt.streams.get_by_itag(ID)
    current = os.getcwd()
    option, options = select_option()
    if option in options:
        for i in options:
            if i == option:
                # options[i](chosen, current)
                pass
    else:
        print("wrong option selected")
        select_option()
    download_option(chosen, current)


def select_option():
    options = {0: download_option, 1: get_link_option}
    option = input("\nSelect preferred option: \n"
                   "     0 => Download \n"
                   "     1 => Get Link \n"
                   "option: ")
    option = int(option)
    return option, options


def get_link_option(chosen, current):
    print(chosen.url)


def download_option(chosen, current):
    folder = set_path(current)
    if folder == "":
        chosen.download('Downloads/Default')
        print("Downloaded! \n")
        safe_start()
    elif folder in default_folders:
        path = default_folders[folder]
        change_path(current, folder)
        chosen.download(f'Downloads/{path}')
        print('Downloaded \n')
        safe_start()
    else:
        change_path(current, folder)
        folder_list(folder)
        chosen.download(f'Downloads/{folder}')
        print("Downloaded! \n")
        safe_start()


def safe_start():
    try:
        start()
    except Exception as e:
        print("\n[ERROR] Please:\n"
              "          - Check VPN Connection\n"
              "          - Change Your Link\n"
              "          - Update Libraries\n")
        print(e)


def folder_list(folder):
    if not default_folders == {}:
        max_num = max(default_folders)
        max_num = int(max_num) + 1
    else:
        max_num = 0
    new_folder = {f"{max_num}": folder}
    default_folders.update(new_folder)


def change_path(current, folder):
    if folder in default_folders:
        joined = os.path.join(current, 'Downloads/', default_folders[folder])
    else:
        joined = os.path.join(current, 'Downloads/', folder)
    print(f"Your Video Will be saved at: {joined} \n")


def set_path(current):
    print(f"\nDefault Folder is: {os.path.join(current, 'Downloads/Default')} \n")
    print(f"These are the folders that you already downloaded videos in \n")
    for i in default_folders:
        print(f"{i} => {default_folders[i]} \n")
    folder = input("Enter Folder name or just leave it for default: ")
    return folder


def get_stream(streams):
    for stream in streams:
        print(f"ID: {stream.itag} | quality: {stream.resolution} | size: {Convertor(size=stream.filesize).convert()}")
    ID = input("Enter The ID: ")
    ID = int(ID)
    return ID


def get_details(yt):
    print(f'Title: {yt.title}')
    print(f'Time: {Time(time=yt.length).convert()}' + "\n")


safe_start()
