import time
import tqdm
import random
import urllib3
import json
import requests

# music.163.com/weapi/song/enhance/player/url?id=1455370222&csrf_token=
# http://music.163.com/song/media/outer/url?id=1455370222.mp3
# https://music.163.com/weapi/song/enhance/player/url?csrf_token=
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}


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


def get_url_from_id(artist_id):
    def id_format(name):
        id_list = []
        step = 0  # 0:normal, 1:i, 2:d, 3:d, 4:', 5:get
        ram = ""
        for i in range(len(name)):
            # print(len(name))
            # print(name[i])
            if name[i] == "'" and step != 3:
                step = 1

            elif name[i] == "i" and step == 1:
                step = 2

            elif name[i] == "d" and step == 2:
                step = 3

            elif name[i] == "'" and step == 3:
                step = 4

            elif step == 4 and name[i] == ':':
                step = 5

            elif step == 5 and name[i] == ' ':
                step = 6

            elif step == 6 and name[i] == ',':
                id_list.append(ram)
                ram = ""
                step = 0

            elif step == 6:
                ram = ram + name[i]

            elif step != 6:
                step = 0
            print(name[i]+'\n'+'step:', step)
        return id_list
    """
    发送请求获取指定歌手的歌曲信息
    参数:
    artist_id (str): 歌手的 ID
    返回:
    list or None: 成功则返回歌曲列表，否则返回 None
    """
    url = 'https://music.163.com/api/v1/artist/songs'  # 歌手歌曲信息 API 的 URL
    params = {
        'id': artist_id,  # 歌手 ID
        'offset': 0,  # 偏移量
        'total': True,  # 是否获取全部歌曲信息
        'limit': 50  # 获取歌曲数量
    }
    try:
        response = requests.get(url, headers=headers, params=params)  # 发送 GET 请求
        response.raise_for_status()  # 如果响应状态码不是 200，抛出异常
        result = json.loads(response.text)  # 将响应的文本内容转为 JSON 格式
        id_list = id_format(str(result))
        print(str(result))
        print(id_list)
    except requests.exceptions.RequestException as e:
        print('请求出错:', e)  # 打印请求错误信息
        return None

'''
name = input("Input the url of the song(s):")
name_list = name_format_f12(name)
id_list = id_format_f12(name)
# print(name_list)
# print(id_list)
if len(id_list) == len(name_list):
    download_from_id(id_list, name_list)
'''
print(get_url_from_id(34332796))
