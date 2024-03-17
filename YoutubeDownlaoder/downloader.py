import math
import os

import requests as requests
from pytube import YouTube
from tqdm import tqdm

from YoutubeDownlaoder.byte_convertor import Convertor
from YoutubeDownlaoder.time_convertor import Time
from .list_files import get as directories_get


class Downloader:
    def __init__(self):
        self.default_download_path = 'Downloads'
        self.default_folders = {}
        self.download = 0

    def get_directories(self):
        folders = directories_get(direction=self.default_download_path)
        if self.default_folders == {}:
            for folder in folders:
                self.folder_list(folder)

    def start(self):
        self.get_directories()
        link = input("Enter Your Link: ")
        if link == "exit":
            exit()
        yt = YouTube(url=link)
        self.get_details(yt)
        streams = yt.streams.filter(progressive=True)
        ID = self.get_stream(streams)
        chosen = yt.streams.get_by_itag(ID)
        current = os.getcwd()
        option, options = self.select_option()
        if option in options:
            options[option](chosen, current, yt)
        else:
            print("wrong option selected")
            self.select_option()

    def select_option(self):
        options = {0: self.download_option, 1: self.get_link_option}
        option = input("\nSelect preferred option: \n"
                       "     0 => Download \n"
                       "     1 => Get Link \n"
                       "option: ")
        option = int(option)
        return option, options

    def get_link_option(self, chosen, current, yt):
        print(chosen.url)

    def download_option(self, chosen, current, yt):
        folder = self.set_path(current)
        if folder == "":
            self.download_file(chosen, path="Downloads/Default", yt=yt)
            print("Downloaded! \n")
            self.safe_start()
        elif folder in self.default_folders:
            path = self.default_folders[folder]
            self.change_path(current, folder)
            self.download_file(chosen, f'Downloads/{path}', yt)
            print('Downloaded \n')
            self.safe_start()
        else:
            self.change_path(current, folder)
            self.folder_list(folder)
            self.download_file(chosen, f'Downloads/{folder}', yt)
            print("Downloaded! \n")
            self.safe_start()

    def safe_start(self):
        try:
            self.start()
        except Exception as e:
            print("\n[ERROR] Please:\n"
                  "          - Check VPN Connection\n"
                  "          - Change Your Link\n"
                  "          - Update Libraries\n")
            print(e)

    def folder_list(self, folder):
        if not self.default_folders == {}:
            max_num = max(self.default_folders)
            max_num = int(max_num) + 1
        else:
            max_num = 0
        new_folder = {f"{max_num}": folder}
        self.default_folders.update(new_folder)

    def change_path(self, current, folder):
        if folder in self.default_folders:
            joined = os.path.join(current, 'Downloads/', self.default_folders[folder])
        else:
            joined = os.path.join(current, 'Downloads/', folder)
        print(f"Your Video Will be saved at: {joined} \n")

    def set_path(self, current):
        print(f"\nDefault Folder is: {os.path.join(current, 'Downloads/Default')} \n")
        print(f"These are the folders that you already downloaded videos in \n")
        for i in self.default_folders:
            print(f"{i} => {self.default_folders[i]} \n")
        folder = input("Enter Folder name or just leave it for default: ")
        return folder

    def get_stream(self, streams):
        for stream in streams:
            print(
                f"ID: {stream.itag} | quality: {stream.resolution} | size: {Convertor(size=stream.filesize).convert()}")
        ID = input("Enter The ID: ")
        ID = int(ID)
        return ID

    # git
    # config - -
    # global user.email
    # "you@example.com"
    # git
    # config - -
    # global user.name
    # "Your Name"

    def get_details(self, yt):
        print(f'Title: {yt.title}')
        print(f'Time: {Time(time=yt.length).convert()}' + "\n")

    def download_file(self, chosen, path, yt):
        url = chosen.url  # big file test
        # Streaming, so we can iterate over the response.
        response = requests.get(url, stream=True)
        total_size_in_bytes = int(response.headers.get('content-length', 0))
        block_size = 1024  # 1 Kibibyte
        progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True, desc="Downloading")
        base_path = os.getcwd()
        download_path = os.path.join(base_path, path)
        if not os.path.exists(download_path):
            os.mkdir(download_path)
        with open(download_path + '/' + yt.title + '.mp4', 'wb') as file:
            for data in response.iter_content(block_size):
                progress_bar.update(len(data))
                file.write(data)
        progress_bar.close()
        if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
            print("ERROR, something went wrong")
