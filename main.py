from YoutubeDownlaoder.downloader import Downloader
import os

if not os.path.isdir('Downloads'):
    os.mkdir('Downloads')

Downloader().safe_start()
