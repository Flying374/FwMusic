#  Author: Flying374
#  Version: 1.1-dev9

import requests
from lxml import etree
import os

from FwMusic_LocalAPI.v1.Artist_info_v1 import Artist
from FwMusic_LocalAPI.v1.Download_from_id_v1 import Downloader

# music.163.com/weapi/song/enhance/player/url?id=1455370222&csrf_token=
# http://music.163.com/song/media/outer/url?id=1455370222.mp3
# https://music.163.com/weapi/song/enhance/player/url?csrf_token=
'''
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Cookie': 'MUSIC_U=1eb9ce22024bb666e99b6743b2222f29ef64a9e88fda0fd5754714b900a5d70d993166e004087dd3b95085f6a85b059f5e9aba41e3f2646e3cebdbec0317df58c119e5;appver=8.9.75;'
}
'''


'''
get_details_from_artist_id  ---  入参:artist_id  出参:[artist_id, artist_name, songs_name_list, songs_id_list]
downlaod_from_id ---  入参:[artist_id, artist_name, songs_name_list, songs_id_list] 出参:None
'''
# <ul class="f-hide"><li><a href="/song?id=1335796886">花间游</a></li><li><a href="/song?id=487864613">寂川</a></li><li><a href="/song?id=1352004027">得似旧时</a></li><li><a href="/song?id=428391474">那年夏天，阳光正好</a></li><li><a href="/song?id=1483533107">薄荷绿</a></li><li><a href="/song?id=1808372495">晴云</a></li><li><a href="/song?id=1860122134">荒川之月</a></li><li><a href="/song?id=2075085097">薰风初昼长</a></li><li><a href="/song?id=515715891">In The Good Times</a></li><li><a href="/song?id=460173322">观灯</a></li><li><a href="/song?id=1300726769">旧事</a></li><li><a href="/song?id=2056529061">再次回到那个夏天</a></li><li><a href="/song?id=1341851239">雪满山中</a></li><li><a href="/song?id=2123300735">没有结局的开始</a></li><li><a href="/song?id=2084455740">须臾之梦</a></li><li><a href="/song?id=1825216246">远书</a></li><li><a href="/song?id=410714365">清月</a></li><li><a href="/song?id=2622641914">凌晨三点的寂静群山</a></li><li><a href="/song?id=1993440849">醒来明月，醉时清风</a></li><li><a href="/song?id=1444647128">我能想到的最幸福的事</a></li><li><a href="/song?id=487866745">暮落（终章）</a></li><li><a href="/song?id=1294799290">夏风微凉</a></li><li><a href="/song?id=1454884913">人间风景</a></li><li><a href="/song?id=1971658643">甜味夏天</a></li><li><a href="/song?id=542818195">回忆之末</a></li><li><a href="/song?id=404459371">浮游于梦</a></li><li><a href="/song?id=1444639931">风中有音</a></li><li><a href="/song?id=1365858944">山桃如雪</a></li><li><a href="/song?id=487866133">朝生（序章）</a></li><li><a href="/song?id=1498649082">一人之境</a></li><li><a href="/song?id=2146742860">黎明到来之前</a></li><li><a href="/song?id=2035130279">她和她的她</a></li><li><a href="/song?id=428387405">以道入魔</a></li><li><a href="/song?id=487864776">雾原</a></li><li><a href="/song?id=864892593">时间飞行 钢琴版</a></li><li><a href="/song?id=556036685">向着朝阳，我走过冬夜寒风</a></li><li><a href="/song?id=1358343231">浮生(inst.)</a></li><li><a href="/song?id=1380302367">流萤</a></li><li><a href="/song?id=487866627">崖居</a></li><li><a href="/song?id=404460258">归风</a></li><li><a href="/song?id=404460260">明镜亦非台</a></li><li><a href="/song?id=515716756">If The Story Ends Well</a></li><li><a href="/song?id=1874430113">梦归</a></li><li><a href="/song?id=2112799613">相逢于时光彼岸</a></li><li><a href="/song?id=2132050270">深海消亡前的诗</a></li><li><a href="/song?id=502569500">破晓</a></li><li><a href="/song?id=1927459179">东池宴</a></li><li><a href="/song?id=1406665130">花开有时</a></li><li><a href="/song?id=1904805030">逆着风</a></li><li><a href="/song?id=409650937">one day the miracle will come</a></li></ul>


def download_from_outer(id):
    pass


def get_details_from_artist_id(artist_id):
    headers = {
        'Referer': 'http://music.163.com',
        'Host': 'music.163.com',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'User-Agent': 'Chrome/10'
    }

    page_url = 'https://music.163.com/artist?id=' + str(artist_id)
    res = requests.get(page_url, headers=headers)
    html = etree.HTML(res.text)
    artist_name = html.xpath("//meta[@name='keywords']/@content")[0]
    href_xpath = "//*[@id='hotsong-list']//a/@href"
    name_xpath = "//*[@id='hotsong-list']//a/text()"
    hrefs = html.xpath(href_xpath)
    names = html.xpath(name_xpath)

    song_ids = [href[9:] for href in hrefs]
    song_names = list(names)
    artist_list = [artist_id, artist_name, song_names, song_ids]
    return  artist_list


def main():
    while True:
        ans = input('>>> ')

        if ans.lower() == 'exit':
            break

        elif ans.lower() == 'download':
            artist_id = input(">>> Input the artist ID: ")
            artist_info = Artist([artist_id, "", [], []])  # Use initial information to create Artist instance
            artist_info.update_info()  # Get and update artist info
            artist_details = artist_info.read_info()  # Read updated info from file

            # Check song information
            artist_name, song_ids, song_names = artist_details[1], artist_details[3], artist_details[2]
            if len(song_ids) == len(song_names):
                print('Artist name:', artist_name)
                print('Starting download...')
                downloader = Downloader(artist_details)  # Create Downloader instance
                downloader.download()  # Download songs
                print('Download completed.')
            else:
                print("Error: The number of songs does not match the number of names.")

        elif ans.lower() == 'update':
            artist_id = input(">>> Input the artist ID: ")
            if artist_id != 'all':
                print('Starting update...')
                artist_info = Artist([artist_id, "", [], []])
                artist_info.update_info()  # Update song info
                artist_details = artist_info.read_info()  # Read updated info

                id_lost, name_lost = artist_info.update_info()  # Perform update and get lost song info
                if id_lost != ['-1'] and name_lost != ['-1']:
                    print('Update completed. The following songs are lost:', id_lost, name_lost)
                    print("Starting download...")
                    downloader = Downloader([artist_id, artist_details[1], name_lost, id_lost])  # Create Downloader instance using lost songs info
                    downloader.download()  # Download lost songs
                    print('Download completed.')
                else:
                    print('An error occurred, unable to update.')
            else:  # If input is 'all'
                with open('../artist_details/all_songs.txt', 'r', encoding='utf-8') as f:  # Ensure the path is correct
                    all_ids = list(eval(f.read()))  # Read all artist IDs
                for id in all_ids:
                    print(f'Starting update for artist ID: {id}...')
                    artist_info = Artist([id, "", [], []])
                    artist_info.update_info()  # Update and get info

                    id_lost, name_lost = artist_info.update_info()  # Get lost song info
                    if id_lost != ['-1'] and name_lost != ['-1']:
                        print('Update completed. The following songs are lost:', id_lost, name_lost)
                        print("Starting download...")
                        downloader = Downloader([id, artist_info.artist_name, name_lost, id_lost])  # Create Downloader instance
                        downloader.download()  # Download lost songs
                        print('Download completed.')
                    else:
                        print(f'An error occurred while updating artist ID {id}.')
            print('Update process completed.')

if __name__ == "__main__":
    main()

