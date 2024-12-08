#  Author:Flying374
import time
import tqdm
import random
import urllib3
import requests
from lxml import etree
import os
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


def download_from_id(artist_id, artist_name, id_list, list_name):
    print(artist_id, artist_name, id_list, list_name)
    def name_format(name):
        name_f = name.replace("/", "-")
        return name_f

    def urllib_download(id, filename):
        url = 'http://music.163.com/song/media/outer/url?id=' + str(id)
        print(url)
        filename = filename + ".mp3"
        connection_pool = urllib3.PoolManager()
        resp = connection_pool.request('GET', url)
        #f = open('music/'+artist_name+'/'+name_format(filename), 'wb')
        #f.write(resp.data)
        #f.close()
        resp.release_conn()

    os.makedirs('music/'+artist_name, exist_ok=True)
    pbar = tqdm.tqdm(total=len(id_list))
    for i in range(len(id_list)):
        urllib_download(id_list[i], list_name[i])
        if i // 4 == 0:
            time.sleep(random.uniform(3, 5))
        time.sleep(random.uniform(2, 5))
        pbar.update(1)
    artist_info(artist_id, 'update')
    pbar.close()


def download_from_outer(id):
    pass

'''
入参：artist_id
返回值：[artist_name, artist_id, song_ids, song_names]
'''
def get_url_from_id(artist_id):
    headers = {
        'Referer': 'http://music.163.com',
        'Host': 'music.163.com',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'User-Agent': 'Chrome/10'
    }

    page_url = 'https://music.163.com/artist?id=' + str(artist_id)
    res = requests.request('GET', page_url, headers=headers)
    html = etree.HTML(res.text)
    artist_name = html.xpath("//meta[@name='keywords']/@content")[0]
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
    return [artist_id,artist_name, song_ids, song_names]


def artist_info(artist_id, usage):  # 保存/提取作者信息到文件
    artist_name, song_ids, song_names = get_url_from_id(artist_id)[1:4]
    #  print(artist_name, song_ids, song_names)
    #  保存歌手信息到文件
    info = [song_ids, song_names]
    with open('/artist_details/all_songs.txt', 'r', encoding='utf-8') as f:
        all_ids = list(eval(f.read()))
        f.close()
    if artist_id not in all_ids:
        all_ids.append(artist_id)
        with open('/artist_details/all_songs.txt', 'w', encoding='utf-8') as f:
            f.write(str(all_ids))
            f.close()

    if usage == 'update':
        with open('/artist_details/' + artist_id + '.txt', 'w', encoding='utf-8') as f:
            f.write(str(info))
            f.close()

        with open('/artist_details/' + artist_id + '_update.txt', 'w', encoding='utf-8') as f:
            time_now = [time.strftime("[%Y, %m, %d, %H, %M, %S]", time.localtime())]
            f.write(str(time_now))
            f.close()

    elif usage == 'read':
        with open('/artist_details/' + artist_id + '.txt', 'w', encoding='utf-8') as f:
            info = list(eval(f.read()))
            f.close()
            with open('/artist_details/' + artist_id + '_update.txt', 'r', encoding='utf-8') as f:
                update_time = list(eval(f.read()))
                f.close()
    return info, update_time


def artist_song_update(artist_id):  # 更新歌手信息并返回缺失歌曲
    [artist_name, song_ids, song_names] = get_url_from_id(artist_id)[1:4]
    #  print(artist_name, song_ids, song_names)
    if os.path.exists('/artist_details/' + artist_id + '.txt'):
        song_ids_old = artist_info(artist_id, 'read')[0]
        song_names_old = artist_info(artist_id, 'read')[1]
        id_lost = []
        name_lost = []
        for i in song_ids:
            if i not in song_ids_old:
                id_lost.append(i)
        for i in song_names:
            if i not in song_names_old:
                name_lost.append(i)
        artist_info(artist_id, 'update')
        if len(id_lost) == len(name_lost):
            return id_lost, name_lost
    else:
        artist_info(artist_id, 'update')
        return ['-1'], ['-1']


'''
name = input("Input the url of the song(s):")
name_list = name_format_f12(name)
id_list = id_format_f12(name)
# print(name_list)
# print(id_list)
if len(id_list) == len(name_list):
    download_from_id(id_list, name_list)

#  print(get_url_from_id(961358))

artist_info(961358, 'write')
print(artist_info(961358,'read'))
# 假设这个函数已经存在，它会处理下载逻辑
artist_id = input("Input the id of the artist:")
artist_name, song_ids, song_names = get_url_from_id(artist_id)
if len(song_ids) == len(song_names):
    print('Artist name is :', artist_name)
    download_from_id(song_ids, song_names)
else:
    print("Error: the number of songs is not equal to the number of names.")
'''

# main
while True:
    ans = input('>>> ')

    if ans == 'exit':
        break

    elif ans == 'download':
        artist_id = input(">>> Input the id of the artist:")
        artist_name, song_ids, song_names = get_url_from_id(artist_id)[1:4]
        if len(song_ids) == len(song_names):
            print('Artist name is :', artist_name)
            print('Start downloading...')
            download_from_id(artist_id, artist_name, song_ids, song_names)
            print('Download completed.')
        else:
            print("Error: the number of songs is not equal to the number of names.")

    elif ans == 'update':
        artist_id = input(">>> Input the id of the artist:")
        if artist_id != 'all':
            print('Start updating...')
            artist_name, id_lost, name_lost = artist_song_update(artist_id)
            if id_lost != ['-1'] and name_lost != ['-1']:
                print('Update completed. The following songs are lost:', id_lost, name_lost)
                print("Start downloading...")
                download_from_id(artist_id, artist_name, id_lost, name_lost)
                print('Download completed.')
            else:
                print('Some error occurred.')
                print('Update completed.')
        elif id == 'all':
            with open('/artist_details/all_songs.txt', 'r', encoding='utf-8') as f:
                all_ids = list(eval(f.read()))
                f.close()
            for id in all_ids:
                artist_name, id_lost, name_lost = artist_song_update(id)
                if id_lost != ['-1'] and name_lost != ['-1']:
                    print('Update completed. The following songs are lost:', id_lost, name_lost)
                    print("Start downloading...")
                    download_from_id(artist_id, artist_name, id_lost, name_lost)
                    print('Download completed.')
                else:
                    print('Some error occurred.')
                    print('Update completed.')
