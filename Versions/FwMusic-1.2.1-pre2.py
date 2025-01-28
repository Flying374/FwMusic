import LocalAPI_v10201 as LocalAPI
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

# <ul class="f-hide"><li><a href="/song?id=1335796886">花间游</a></li><li><a href="/song?id=487864613">寂川</a></li><li><a href="/song?id=1352004027">得似旧时</a></li><li><a href="/song?id=428391474">那年夏天，阳光正好</a></li><li><a href="/song?id=1483533107">薄荷绿</a></li><li><a href="/song?id=1808372495">晴云</a></li><li><a href="/song?id=1860122134">荒川之月</a></li><li><a href="/song?id=2075085097">薰风初昼长</a></li><li><a href="/song?id=515715891">In The Good Times</a></li><li><a href="/song?id=460173322">观灯</a></li><li><a href="/song?id=1300726769">旧事</a></li><li><a href="/song?id=2056529061">再次回到那个夏天</a></li><li><a href="/song?id=1341851239">雪满山中</a></li><li><a href="/song?id=2123300735">没有结局的开始</a></li><li><a href="/song?id=2084455740">须臾之梦</a></li><li><a href="/song?id=1825216246">远书</a></li><li><a href="/song?id=410714365">清月</a></li><li><a href="/song?id=2622641914">凌晨三点的寂静群山</a></li><li><a href="/song?id=1993440849">醒来明月，醉时清风</a></li><li><a href="/song?id=1444647128">我能想到的最幸福的事</a></li><li><a href="/song?id=487866745">暮落（终章）</a></li><li><a href="/song?id=1294799290">夏风微凉</a></li><li><a href="/song?id=1454884913">人间风景</a></li><li><a href="/song?id=1971658643">甜味夏天</a></li><li><a href="/song?id=542818195">回忆之末</a></li><li><a href="/song?id=404459371">浮游于梦</a></li><li><a href="/song?id=1444639931">风中有音</a></li><li><a href="/song?id=1365858944">山桃如雪</a></li><li><a href="/song?id=487866133">朝生（序章）</a></li><li><a href="/song?id=1498649082">一人之境</a></li><li><a href="/song?id=2146742860">黎明到来之前</a></li><li><a href="/song?id=2035130279">她和她的她</a></li><li><a href="/song?id=428387405">以道入魔</a></li><li><a href="/song?id=487864776">雾原</a></li><li><a href="/song?id=864892593">时间飞行 钢琴版</a></li><li><a href="/song?id=556036685">向着朝阳，我走过冬夜寒风</a></li><li><a href="/song?id=1358343231">浮生(inst.)</a></li><li><a href="/song?id=1380302367">流萤</a></li><li><a href="/song?id=487866627">崖居</a></li><li><a href="/song?id=404460258">归风</a></li><li><a href="/song?id=404460260">明镜亦非台</a></li><li><a href="/song?id=515716756">If The Story Ends Well</a></li><li><a href="/song?id=1874430113">梦归</a></li><li><a href="/song?id=2112799613">相逢于时光彼岸</a></li><li><a href="/song?id=2132050270">深海消亡前的诗</a></li><li><a href="/song?id=502569500">破晓</a></li><li><a href="/song?id=1927459179">东池宴</a></li><li><a href="/song?id=1406665130">花开有时</a></li><li><a href="/song?id=1904805030">逆着风</a></li><li><a href="/song?id=409650937">one day the miracle will come</a></li></ul>


Supported_api_version = 'v10201_p2'
Api = LocalAPI.API()


if Api.get_version() != Supported_api_version:
	print("ErrA1 : LocalAPI Version doesn't match Program version.")
	print('Now the version is :' + Api.get_version() + '.')
	print('Please use :' + Supported_api_version + '.')
	exit()

Errinfo = LocalAPI.ErrInfo()
Flog = LocalAPI.FLog()
Flog.create()

'''
def download_from_id(artist_id, type):
	def name_format(name):
		name_f = name.replace("/", "-")
		return name_f

	def urllib_download(id, filename):
		try:
			url = 'http://music.163.com/song/media/outer/url?id=' + str(id)
			# print(url)
			filename = filename + ".mp3"
			connection_pool = urllib3.PoolManager()
			resp = connection_pool.request('GET', url)
			music = open('Music/'+artist_name+'/'+name_format(filename), 'wb')
			music.write(resp.data)
			music.close()
			resp.release_conn()
		except Exception:
			print('ErrUD1' + Errinfo.solve('ErrUD1'))
			Flog.failure('ErrUD1 :' + Errinfo.solve('ErrUD1'))

	def download(all_list):
		os.makedirs('Music', exist_ok=True)
		for i in range(len(all_list)):
			urllib_download(all_list[i][1], all_list[i][0])
			Flog.info('Downloading' + all_list[i][0] + ', id=' + all_list[i][1] + '.')
			if i // 4 == 0:
				time.sleep(random.uniform(3, 5))
			time.sleep(random.uniform(3, 6))
			pbar.update(1)
	
	artist = LocalAPI.Artist(artist_id)
	Flog.info('Get details from artist , id:' + str(artist_id))
	artist.get_details()
	print(artist.get_songs())

	if artist.read('old') == 'ErrR1': #  first time
		Flog.warning('ErrR1 :' + Errinfo.solve('ErrR1'))
		download(artist.get_songs())
		artist.save(True)

	elif artist.read('old') != 'ErrR1':
		if type == 'all':
			download(artist.read('new'))
			artist.save(True)
		elif type == 'new':
			download(artist.read('newer'))
			artist.save(True)
		elif type == 'old':
			download(artist.read('old'))
			artist.save(True)

'''
# download_from_id(12611210, 'all')
artist_id = 12611210
artist = LocalAPI.Artist(artist_id)
Flog.info('Get details from artist , id:' + str(artist_id))
artist.get_details()
artist.save(True)
# print(artist.get_songs())
