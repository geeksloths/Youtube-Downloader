from pytube import YouTube as yt

yt = yt(url="https://m.youtube.com/watch?v=f1R_bykXHGE")
chosen = yt.streams.get_by_itag(22)
print(chosen)
