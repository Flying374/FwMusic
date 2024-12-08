import time
import tqdm
import random
import urllib3
import requests
from lxml import etree
from werkzeug.http import parse_cookie

# music.163.com/weapi/song/enhance/player/url?id=1455370222&csrf_token=
# http://music.163.com/song/media/outer/url?id=1455370222.mp3
# https://music.163.com/weapi/song/enhance/player/url?csrf_token=
'''
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Cookie': 'MUSIC_U=1eb9ce22024bb666e99b6743b2222f29ef64a9e88fda0fd5754714b900a5d70d993166e004087dd3b95085f6a85b059f5e9aba41e3f2646e3cebdbec0317df58c119e5;appver=8.9.75;'
}
'''

def name_format(name):  # ver:1.0.0
    name_list = []
    ram = ""
    for i in range(len(name)):
        if name[i] == "/":
            name_list.append(ram)
            ram = ""
        else:
            ram = ram + name[i]

    name_list.append(ram)
    return name_list


def name_format_f12(name):  # ver:1.0.0
    name_list = []
    step = 0  # 0:normal, 1:<, 2:l, 3:i, 4:>, 5:<, 6:>, 7:get
    ram = ""
    for i in range(len(name)):
        # print(len(name))
        # print(name[i])
        if name[i] == "<" and step != 4 and step != 5 and step != 6:
            step = 1

        elif name[i] == "l" and step == 1:
            step = 2

        elif name[i] == "i" and step == 2:
            step = 3

        elif name[i] == ">" and step == 3:
            step = 4

        elif name[i] == "<" and step == 4:
            step = 5

        elif name[i] == ">" and step == 5:
            step = 6

        elif name[i] == "<" and step == 6:
            name_list.append(ram)
            ram = ""
            step = 0
            print()

        elif step == 6:
            ram = ram + name[i]

        elif step != 4 and step != 5 and step != 6:
            step = 0
        # print('step:', step)
    return name_list


def id_format_f12(name):  # ver:1.0.0
    id_list = []
    step = 0  # 0:normal, 1:?, 2:i, 3:d, 4:=, 5:get
    ram = ""
    for i in range(len(name)):
        # print(len(name))
        # print(name[i])
        if name[i] == "?":
            step = 1

        elif name[i] == "i" and step == 1:
            step = 2

        elif name[i] == "d" and step == 2:
            step = 3

        elif name[i] == "=" and step == 3:
            step = 4

        elif step == 4 and name[i] == '"':
            id_list.append(ram)
            ram = ""
            step = 0

        elif step == 4:
            ram = ram + name[i]

        elif step != 4:
            step = 0
        # print(name[i]+'\n'+'step:', step)
    return id_list


# <ul class="f-hide"><li><a href="/song?id=1335796886">花间游</a></li><li><a href="/song?id=487864613">寂川</a></li><li><a href="/song?id=1352004027">得似旧时</a></li><li><a href="/song?id=428391474">那年夏天，阳光正好</a></li><li><a href="/song?id=1483533107">薄荷绿</a></li><li><a href="/song?id=1808372495">晴云</a></li><li><a href="/song?id=1860122134">荒川之月</a></li><li><a href="/song?id=2075085097">薰风初昼长</a></li><li><a href="/song?id=515715891">In The Good Times</a></li><li><a href="/song?id=460173322">观灯</a></li><li><a href="/song?id=1300726769">旧事</a></li><li><a href="/song?id=2056529061">再次回到那个夏天</a></li><li><a href="/song?id=1341851239">雪满山中</a></li><li><a href="/song?id=2123300735">没有结局的开始</a></li><li><a href="/song?id=2084455740">须臾之梦</a></li><li><a href="/song?id=1825216246">远书</a></li><li><a href="/song?id=410714365">清月</a></li><li><a href="/song?id=2622641914">凌晨三点的寂静群山</a></li><li><a href="/song?id=1993440849">醒来明月，醉时清风</a></li><li><a href="/song?id=1444647128">我能想到的最幸福的事</a></li><li><a href="/song?id=487866745">暮落（终章）</a></li><li><a href="/song?id=1294799290">夏风微凉</a></li><li><a href="/song?id=1454884913">人间风景</a></li><li><a href="/song?id=1971658643">甜味夏天</a></li><li><a href="/song?id=542818195">回忆之末</a></li><li><a href="/song?id=404459371">浮游于梦</a></li><li><a href="/song?id=1444639931">风中有音</a></li><li><a href="/song?id=1365858944">山桃如雪</a></li><li><a href="/song?id=487866133">朝生（序章）</a></li><li><a href="/song?id=1498649082">一人之境</a></li><li><a href="/song?id=2146742860">黎明到来之前</a></li><li><a href="/song?id=2035130279">她和她的她</a></li><li><a href="/song?id=428387405">以道入魔</a></li><li><a href="/song?id=487864776">雾原</a></li><li><a href="/song?id=864892593">时间飞行 钢琴版</a></li><li><a href="/song?id=556036685">向着朝阳，我走过冬夜寒风</a></li><li><a href="/song?id=1358343231">浮生(inst.)</a></li><li><a href="/song?id=1380302367">流萤</a></li><li><a href="/song?id=487866627">崖居</a></li><li><a href="/song?id=404460258">归风</a></li><li><a href="/song?id=404460260">明镜亦非台</a></li><li><a href="/song?id=515716756">If The Story Ends Well</a></li><li><a href="/song?id=1874430113">梦归</a></li><li><a href="/song?id=2112799613">相逢于时光彼岸</a></li><li><a href="/song?id=2132050270">深海消亡前的诗</a></li><li><a href="/song?id=502569500">破晓</a></li><li><a href="/song?id=1927459179">东池宴</a></li><li><a href="/song?id=1406665130">花开有时</a></li><li><a href="/song?id=1904805030">逆着风</a></li><li><a href="/song?id=409650937">one day the miracle will come</a></li></ul>


def download_from_id(id_list, list_name):
    def name_format(name):
        name_f = ""
        for i in range(len(name)):
            if name[i] == "/":
                name_f = name_f + "-"
            else:
                name_f += name[i]
        return name_f

    def urllib_download(id, filename):
        url = 'http://music.163.com/song/media/outer/url?id=' + str(id)
        filename = filename + ".mp3"
        connection_pool = urllib3.PoolManager()
        resp = connection_pool.request('GET', url)
        f = open(name_format(filename), 'wb')
        f.write(resp.data)
        f.close()
        resp.release_conn()

    pbar = tqdm.tqdm(total=len(id_list))
    for i in range(len(id_list)):
        urllib_download(id_list[i], list_name[i])
        if i // 4 == 0:
            time.sleep(random.uniform(3, 5))
        time.sleep(random.uniform(2, 5))
        pbar.update(1)
    pbar.close()


def download_from_outer(id):
    pass


def get_url_from_id(artist_id):
    headers = {
        'Referer': 'http://music.163.com',
        'Host': 'music.163.com',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'User-Agent': 'Chrome/10'
    }

    page_url = 'https://music.163.com/artist?id=' + str(artist_id)
    # 获取对应HTML
    res = requests.request('GET', page_url, headers=headers)
    # XPath解析 前50的热门歌曲
    html = etree.HTML(res.text)
    href_xpath = "//*[@id='hotsong-list']//a/@href"
    name_xpath = "//*[@id='hotsong-list']//a/text()"
    hrefs = html.xpath(href_xpath)
    names = html.xpath(name_xpath)
    # 设置热门歌曲的ID，歌曲名称
    song_ids = []
    song_names = []
    for href, name in zip(hrefs, names):
        song_ids.append(href[9:])
        song_names.append(name)
        #  print(href, ' ', name) #debug only
    return song_ids, song_names


'''
name = input("Input the url of the song(s):")
name_list = name_format_f12(name)
id_list = id_format_f12(name)
# print(name_list)
# print(id_list)
if len(id_list) == len(name_list):
    download_from_id(id_list, name_list)
'''
'''
# print(get_url_from_id(34332796))

# 假设这个函数已经存在，它会处理下载逻辑
artist_id = input("Input the id of the artist:")
song_ids, song_names = get_url_from_id(artist_id)
if len(song_ids) == len(song_names):
    download_from_id(song_ids, song_names)
else:
    print("Error: the number of songs is not equal to the number of names.")
'''

def download_vip():
    from flask import Flask, request, jsonify, redirect, Response
    import json
    import os
    import urllib.parse
    from hashlib import md5
    from random import randrange
    import requests
    from cryptography.hazmat.primitives import padding
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

    def HexDigest(data):
        return "".join([hex(d)[2:].zfill(2) for d in data])

    def HashDigest(text):
        HASH = md5(text.encode("utf-8"))
        return HASH.digest()

    def HashHexDigest(text):
        return HexDigest(HashDigest(text))

    def ids(ids):
        if '163cn.tv' in ids:
            response = requests.get(ids, allow_redirects=False)
            ids = response.headers.get('Location')
        if 'music.163.com' in ids:
            index = ids.find('id=') + 3
            ids = ids[index:].split('&')[0]
        return ids

    def read_cookie():
        script_dir = os.path.dirname(os.path.abspath(__file__))
        cookie_file = os.path.join(script_dir, 'cookie.txt')
        with open(cookie_file, 'r') as f:
            cookie_contents = f.read()
        return cookie_contents

    def post(url, params, cookie):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Safari/537.36 Chrome/91.0.4472.164 NeteaseMusicDesktop/2.10.2.200154',
            'Referer': '',
        }
        cookies = {
            "os": "pc",
            "appver": "",
            "osver": "",
            "deviceId": "pyncm!"
        }
        cookies.update(cookie)
        response = requests.post(url, headers=headers, cookies=cookies, data={"params": params})
        return response.text

    # 输入id选项
    def ids(ids):
        if '163cn.tv' in ids:
            response = requests.get(ids, allow_redirects=False)
            ids = response.headers.get('Location')
        if 'music.163.com' in ids:
            index = ids.find('id=') + 3
            ids = ids[index:].split('&')[0]
        return ids

    # 转换文件大小
    def size(value):
        units = ["B", "KB", "MB", "GB", "TB", "PB"]
        size = 1024.0
        for i in range(len(units)):
            if (value / size) < 1:
                return "%.2f%s" % (value, units[i])
            value = value / size
        return value

    # 转换音质
    def music_level1(value):
        if value == 'standard':
            return "标准音质"
        elif value == 'exhigh':
            return "极高音质"
        elif value == 'lossless':
            return "无损音质"
        elif value == 'hires':
            return "Hires音质"
        elif value == 'sky':
            return "沉浸环绕声"
        elif value == 'jyeffect':
            return "高清环绕声"
        elif value == 'jymaster':
            return "超清母带"
        else:
            return "未知音质"

    def url_v1(id, level, cookies):
        url = "https://interface3.music.163.com/eapi/song/enhance/player/url/v1"
        AES_KEY = b"e82ckenh8dichen8"
        config = {
            "os": "pc",
            "appver": "",
            "osver": "",
            "deviceId": "pyncm!",
            "requestId": str(randrange(20000000, 30000000))
        }

        payload = {
            'ids': [id],
            'level': level,
            'encodeType': 'flac',
            'header': json.dumps(config),
        }

        if level == 'sky':
            payload['immerseType'] = 'c51'

        url2 = urllib.parse.urlparse(url).path.replace("/eapi/", "/api/")
        digest = HashHexDigest(f"nobody{url2}use{json.dumps(payload)}md5forencrypt")
        params = f"{url2}-36cd479b6b5-{json.dumps(payload)}-36cd479b6b5-{digest}"
        padder = padding.PKCS7(algorithms.AES(AES_KEY).block_size).padder()
        padded_data = padder.update(params.encode()) + padder.finalize()
        cipher = Cipher(algorithms.AES(AES_KEY), modes.ECB())
        encryptor = cipher.encryptor()
        enc = encryptor.update(padded_data) + encryptor.finalize()
        params = HexDigest(enc)
        response = post(url, params, cookies)
        return json.loads(response)

    def name_v1(id):
        # 歌曲信息接口
        urls = "https://interface3.music.163.com/api/v3/song/detail"
        data = {'c': json.dumps([{"id": id, "v": 0}])}
        response = requests.post(url=urls, data=data)
        return response.json()

    def lyric_v1(id, cookies):
        # 歌词接口
        url = "https://interface3.music.163.com/api/song/lyric"
        data = {'id': id, 'cp': 'false', 'tv': '0', 'lv': '0', 'rv': '0', 'kv': '0', 'yv': '0', 'ytv': '0', 'yrv': '0'}
        response = requests.post(url=url, data=data, cookies=cookies)
        return response.json()


    def Song_v1(song_ids, url, level, type_):

        if not song_ids and not url:
            return jsonify({'error': '必须提供 ids 或 url 参数'}), 400
        if level is None:
            return jsonify({'error': 'level参数为空'}), 400
        if type_ is None:
            return jsonify({'error': 'type参数为空'}), 400

        jsondata = song_ids if song_ids else url
        cookies = parse_cookie(read_cookie())
        urlv1 = url_v1(ids(jsondata), level, cookies)
        namev1 = name_v1(urlv1['data'][0]['id'])
        lyricv1 = lyric_v1(urlv1['data'][0]['id'], cookies)

        if urlv1['data'][0]['url'] is not None:
            if namev1['songs']:
                song_url = urlv1['data'][0]['url']
                song_name = namev1['songs'][0]['name']
                song_picUrl = namev1['songs'][0]['al']['picUrl']
                song_alname = namev1['songs'][0]['al']['name']
                artist_names = []
                for song in namev1['songs']:
                    ar_list = song['ar']
                    if len(ar_list) > 0:
                        artist_names.append('/'.join(ar['name'] for ar in ar_list))
                    song_arname = ', '.join(artist_names)
        else:
            data = jsonify({"status": 400, 'msg': '信息获取不完整！'}), 400
        if type_ == 'text':
            data = '歌曲名称：' + song_name + '<br>歌曲图片：' + song_picUrl + '<br>歌手：' + song_arname + '<br>歌曲专辑：' + song_alname + '<br>歌曲音质：' + music_level1(
                urlv1['data'][0]['level']) + '<br>歌曲大小：' + size(
                urlv1['data'][0]['size']) + '<br>音乐地址：' + song_url
        elif type_ == 'down':
            data = redirect(song_url)
        elif type_ == 'json':
            data = {
                "status": 200,
                "name": song_name,
                "pic": song_picUrl,
                "ar_name": song_arname,
                "al_name": song_alname,
                "level": music_level1(urlv1['data'][0]['level']),
                "size": size(urlv1['data'][0]['size']),
                "url": song_url,
                "lyric": lyricv1['lrc']['lyric'],
                "tlyric": lyricv1['tlyric']['lyric']
            }
            json_data = json.dumps(data)
            data = Response(json_data, content_type='application/json')
        else:
            data = jsonify({"status": 400, 'msg': '解析失败！请检查参数是否完整！'}), 400
        return data
    Song_v1('', 'https://music.163.com/#/song?id=492390949', 'standard', 'down')

download_vip()
