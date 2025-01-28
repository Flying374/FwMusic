import os
import requests
from lxml import etree


class Artist:
    def __init__(self, artist_list):
        self.artist_id = artist_list[0]
        self.artist_name = artist_list[1]
        self.songs_name_list = artist_list[2]
        self.songs_id_list = artist_list[3]

        # 确保 ../../artist_details 目录存在
        self.artist_details_dir = os.path.join('..', '..', 'artist_details')
        os.makedirs(self.artist_details_dir, exist_ok=True)  # 自动创建目录

    def save_info(self):
        """保存艺术家信息到文件"""
        info = [self.artist_id, self.artist_name, self.songs_name_list, self.songs_id_list]

        # 更新 all_artist_ids.txt
        all_artist_ids_path = os.path.join(self.artist_details_dir, 'all_artist_ids.txt')
        if not os.path.exists(all_artist_ids_path):  # 文件不存在时创建
            with open(all_artist_ids_path, 'w', encoding='utf-8') as f:
                f.write('[]')  # 初始化为空列表

        with open(all_artist_ids_path, 'r', encoding='utf-8') as f:
            all_ids = list(eval(f.read()))
            if self.artist_id not in all_ids:
                all_ids.append(self.artist_id)

        with open(all_artist_ids_path, 'w', encoding='utf-8') as f:
            f.write(str(all_ids))

        # 保存艺术家信息到文件
        with open(os.path.join(self.artist_details_dir, f'{self.artist_id}.txt'), 'w', encoding='utf-8') as f:
            f.write(str(info))  # 直接写入所需格式

    def update_info(self):
        """更新艺术家的歌曲信息并返回缺失的歌曲"""
        headers = {
            'Referer': 'http://music.163.com',
            'Host': 'music.163.com',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'User-Agent': 'Chrome/10'
        }
        page_url = f'https://music.163.com/artist?id={self.artist_id}'
        res = requests.get(page_url, headers=headers)
        html = etree.HTML(res.text)
        artist_name = html.xpath("//meta[@name='keywords']/@content")[0]
        href_xpath = "//*[@id='hotsong-list']//a/@href"
        name_xpath = "//*[@id='hotsong-list']//a/text()"
        hrefs = html.xpath(href_xpath)
        names = html.xpath(name_xpath)

        song_ids = [href[9:] for href in hrefs]
        song_names = list(names)

        new_artist_info = [self.artist_id, artist_name, song_names, song_ids]
        new_song_ids = new_artist_info[3]
        new_song_names = new_artist_info[2]

        id_lost = []
        name_lost = []

        # 读取旧信息
        if os.path.exists(os.path.join(self.artist_details_dir, f'{self.artist_id}.txt')):
            old_info = self.read_info()  # 读取旧信息
            old_artist_id = old_info[0]
            old_artist_name = old_info[1]
            old_song_ids = old_info[3]  # 根据新的格式获取旧歌曲 IDs
            old_song_names = old_info[2]  # 根据新的格式获取旧歌曲名字

            # 检查缺失的歌曲
            for song_id in new_song_ids:
                if song_id not in old_song_ids:
                    id_lost.append(song_id)
            for song_name in new_song_names:
                if song_name not in old_song_names:
                    name_lost.append(song_name)

            self.save_info()  # 保存最新的信息
        else:
            self.save_info()  # 保存新的信息
            return ['-1'], ['-1']

        return id_lost, name_lost  # 返回缺失歌曲的 ID 和名称

    def read_info(self):
        """读取艺术家的信息"""
        with open(os.path.join(self.artist_details_dir, f'{self.artist_id}.txt'), 'r', encoding='utf-8') as f:
            info = list(eval(f.read()))

        return info  # 返回读取的信息，格式为 [artist_id, artist_name, songs_name_list, songs_id_list]



