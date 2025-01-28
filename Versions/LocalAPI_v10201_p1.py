#  LocalAPI v.10201
#  Author: Flying374
import time
import tqdm
import random
import urllib3
import requests
from lxml import etree
import os


# music.163.com/weapi/song/enhance/player/url?id=1455370222&csrf_token=
# http://music.163.com/song/media/outer/url?id=1455370222.mp3
# https://music.163.com/weapi/song/enhance/player/url?csrf_token=
class API:
    def __init__(self):
        self.__VersionDictionary = {'API': 'v10201',
                                    'ArtistAPI': '2.0.1(250122)',
                                    'ErrInfoAPI': 'v1.0(250117)',
                                    'FLogAPI': 'v1.3(250117)',
                                    'MusicListAPI': 'v1.0(250117)',
                                    }

    def get_version(self):
        return self.__VersionDictionary['API']

    def get_version_dictionary(self):
        return self.__VersionDictionary


Api = API()


class Artist:
    def __init__(self, artist_id):
        self.artist_id = artist_id
        self.artist_name = 'Default'
        self.artist_songs = []  # [[song_name, song_id, author_name, author_id, is_vip]]

    def get_name(self):
        return self.artist_name

    def get_id(self):
        return self.artist_id

    def get_songs(self):
        #  print(self.artist_songs) #debug only
        return self.artist_songs

    def get_details(self):
        artist_id = self.artist_id
        try:
            headers = {
                'Referer': 'http://music.163.com',
                'Host': 'music.163.com',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'User-Agent': 'Chrome/10'
            }
            page_url = 'https://music.163.com/artist?id=' + str(artist_id)  # no/#/, it's a bug
            res = requests.request('GET', page_url, headers=headers)
            html = etree.HTML(res.text)
            artist_name = html.xpath("//meta[@name='keywords']/@content")[0]
            href_xpath = "//*[@id='hotsong-list']//a/@href"
            name_xpath = "//*[@id='hotsong-list']//a/text()"
            hrefs = html.xpath(href_xpath)
            names = html.xpath(name_xpath)
            song_ids = []
            song_names = []
            # print(song_ids, song_names)  # debug only
            for href, name in zip(hrefs, names):
                song_ids.append(href[9:])
                song_names.append(name)
                # print(href, ' ', name)  # debug only
            artist_songs = []
            if len(song_names) == len(song_ids):
                for i in range(len(song_names)):
                    artist_songs.append([song_names[i], song_ids[i], artist_name, artist_id, False])
            else:
                return 'ErrG2'
            self.artist_id = artist_id
            self.artist_name = artist_name
            self.artist_songs = artist_songs
        except Exception:
            # print('ErrG1')
            return 'ErrG1'

    def save(self, do_force_update):
        artist_id = self.artist_id
        artist_songs = self.artist_songs
        path = os.path.join('Artists', str(artist_id) + '.txt')
        # print(path)
        os.makedirs('Artists', exist_ok=True)
        if os.path.exists(path):
            if do_force_update:
                f = open(path, 'w+')  # Write only.
                f.write(str(artist_songs))
                f.close()
            elif not do_force_update:
                with open(path, 'r+', encoding="utf-8") as f:
                    data = f.read()
                    artist_songs_old = eval(data)
                    artist_songs_new = artist_songs_old[:]
                    for i in artist_songs:
                        if not i in artist_songs_new:
                            artist_songs_new.append(i)
                    f.close()
                f = open(path, 'w+')  # Write only.
                f.write(str(artist_songs_new))
                f.close()

        else:
            f = open(path, 'w+')  # Write only.
            f.write(str(artist_songs))
            f.close()

    def read(self, return_type):
        artist_id = self.artist_id
        artist_songs = self.artist_songs
        path = os.path.join('Artists', str(artist_id) + '.txt')
        # print(path)
        os.makedirs('Artists', exist_ok=True)
        if os.path.exists(path):
            with open(path, 'r+', encoding="utf-8") as f:
                data = f.read()
                artist_songs_old = eval(data)
                artist_songs_new = artist_songs_old[:]
                artist_songs_newer = []
                for i in artist_songs:
                    if not i in artist_songs_new:
                        artist_songs_new.append(i)
                for i in artist_songs:
                    if not i in artist_songs_old:
                        artist_songs_newer.append(i)
                f.close()

                if return_type == 'old':
                    return artist_songs_old

                elif return_type == 'new':
                    return artist_songs_new

                elif return_type == 'newer':
                    return artist_songs_newer

        else:
            f = open(path, 'w+')  # Write only.
            f.write(str(artist_songs))
            f.close()
            return ('ErrR1')


class ErrInfo:
    def __init__(self):
        self.__ErrDictionary = {'ErrR1': 'File does NOT exist.',
                                'ErrG1': 'Fail to get details from (https://music.163.com/#/artist?id=).',
                                'ErrG2': "Information aren't in right forms.",
                                'ErrE1': 'Error type is not in list.',
                                'ErrA1': "LocalAPI Version doesn't match Program version.",
                                'ErrUD1': 'Can not download music from 163music.',
                                'ErrML1': 'Artist file does NOT exist.'
                                }

    def solve(self, ErrType):
        try:
            return self.__ErrDictionary[ErrType]

        except Exception:
            return 'ErrE1'


class FLog:
    def __init__(self):
        self.log_time = str(time.strftime('%Y-%m-%d-%H-%M-%S'))
        self.path = os.path.join('Logs', self.log_time + '.txt')

    def create(self):
        os.makedirs('Logs', exist_ok=True)
        path = self.path
        log = open(path, 'a')
        log.write('[INFO] (' + str(time.strftime('%Y-%m-%d %H:%M:%S')) + \
                  ') Start FwMusic.' + '\n')

        log.write('[INFO] (' + str(time.strftime('%Y-%m-%d %H:%M:%S')) + \
                  ') API Version:' + Api.get_version_dictionary()['API'] + '.' + '\n')

        log.write('[INFO] (' + str(time.strftime('%Y-%m-%d %H:%M:%S')) + \
                  ') ArtistAPI Version:' + Api.get_version_dictionary()['ArtistAPI'] + '.' + '\n')

        log.write('[INFO] (' + str(time.strftime('%Y-%m-%d %H:%M:%S')) + \
                  ') ErrInfoAPI Version:' + Api.get_version_dictionary()['ErrInfoAPI'] + '.' + '\n')

        log.write('[INFO] (' + str(time.strftime('%Y-%m-%d %H:%M:%S')) + \
                  ') FLogAPI Version:' + Api.get_version_dictionary()['FLogAPI'] + '.' + '\n')

        log.close()

    def info(self, msg):
        path = self.path
        log = open(path, 'a')
        log.write('[INFO] (' + str(time.strftime('%Y-%m-%d %H:%M:%S')) + \
                  ')' + str(msg) + '\n')

    def warning(self, msg):
        path = self.path
        log = open(path, 'a')
        log.write('[WARNING] (' + str(time.strftime('%Y-%m-%d %H:%M:%S')) + \
                  ')' + str(msg) + '\n')

    def failure(self, msg):
        path = self.path
        log = open(path, 'a')
        log.write('[FAILURE] (' + str(time.strftime('%Y-%m-%d %H:%M:%S')) + \
                  ')' + str(msg) + '\n')


class Musiclist:
    def __init__(self):
        self.music_list = []
        self.playlist_name = 'Default'

    def load_artist(self, artist_id):
        artist_file = os.path.join('Artists', str(artist_id) + '.txt')
        if os.path.exists(artist_file):
            with open(artist_file, 'r+', encoding="utf-8") as f:
                data = f.read()
                artist_songs = eval(data)
                for i in artist_songs:
                    self.music_list.append(i)
                f.close()
        else:
            return 'ErrML1'

    def load_from_save(self):
        save_file_name = self.playlist_name + '_playlist'
        os.makedirs('Saves', exist_ok=True)
        save_file = os.path.join('Saves', save_file_name + '.txt')
        if os.path.exists(save_file):
            with open(save_file, 'r+', encoding="utf-8") as f:
                data = f.read()
                self.music_list = eval(data)
                f.close()
        else:
            return 'ErrML1'

    def save(self, name):
        os.makedirs('Saves', exist_ok=True)
        save_file = os.path.join('Saves', name + '.txt')
        f = open(save_file, 'w+')  # Write only.
        f.write(str(self.music_list))
        f.close()

    def clear(self):
        self.music_list = []

    def rename(self, new_name):
        self.playlist_name = new_name

    def add(self, add_list):
        self.music_list.extend(add_list)

    def read(self):
        return self.music_list

    def urllib_download(self, pbar):
        playlist_name = self.playlist_name
        def name_format(name):
            name_f = name.replace("/", "-")
            return name_f

        def urllib_download(id, filename):
            url = 'http://music.163.com/song/media/outer/url?id=' + str(id)
            print(url)
            filename = filename + ".mp3"
            connection_pool = urllib3.PoolManager()
            resp = connection_pool.request('GET', url)
            file = open('music/'+playlist_name+'/'+name_format(filename), 'wb')
            file.write(resp.data)
            file.close()
            resp.release_conn()

        os.makedirs('music/' + artist_name, exist_ok=True)
        for i in range(len(id_list)):
            urllib_download(id_list[i], list_name[i])
            if i // 4 == 0:
                time.sleep(random.uniform(3, 5))
            time.sleep(random.uniform(2, 5))
            pbar.update(1)
        pbar.close()
