import os
import random
import time
import urllib3
import tqdm

class Downloader:
    def __init__(self, artist_list):
        self.artist_id, self.artist_name, self.songs_name_list, self.songs_id_list = artist_list

    def download(self):
        print(f"Downloading songs for artist ID: {self.artist_id}, Artist Name: {self.artist_name}")
        pbar = tqdm.tqdm(total=len(self.songs_id_list))

        for i in range(len(self.songs_id_list)):
            self.urllib_download(self.songs_id_list[i], self.songs_name_list[i])
            time.sleep(random.uniform(3, 6))  # 下载间隔
            if i % 5 == 0:  # 修改为按每5个下载一次
                time.sleep(random.uniform(2, 4))
            pbar.update(1)

        pbar.close()

    def name_format(self, name):
        name = name.replace("<", "《")
        name = name.replace(">", "》")
        name = name.replace(":", ".")
        name = name.replace("/", "-")
        name = name.replace("!", "！")
        name = name.replace("?", "？")
        return name

    def urllib_download(self, song_id, song_name):
        url = f'http://music.163.com/song/media/outer/url?id={str(song_id)}'
        filename = f"{self.name_format(song_name)}.mp3"
        print(f"Downloading from URL: {url}")

        connection_pool = urllib3.PoolManager()
        resp = connection_pool.request('GET', url)

        os.makedirs(f'music/{self.artist_name}', exist_ok=True)
        with open(f'music/{self.artist_name}/{filename}', 'wb') as f:
            f.write(resp.data)

        resp.release_conn()

# 使用示例
# artist_list = [artist_id, artist_name, songs_name_list, songs_id_list]
# downloader = Downloader(artist_list)
# downloader.download()
