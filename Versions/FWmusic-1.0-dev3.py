from playwright.sync_api import sync_playwright
import time
import pyautogui
import random


def download(page, name):
    show = page.locator('#div')
    show.click()
    with page.expect_download() as download_info:
        download_btn = page.get_by_text("下载").first
        download_btn.click()
        download = download_info.value
        download.save_as(name + ".mp3")


def download_click(page, name, x_1, y_1, x_2, y_2):
    time.sleep(5)
    with page.expect_download() as download_info:
        pyautogui.click(x_1, y_1)
        time.sleep(1)
        pyautogui.moveTo(x_2, y_2)
        pyautogui.click()
    download = download_info.value
    download.save_as(name + ".mp3")
    print("download complete.")
    time.sleep(random.randint(1, 3))


def steal_music_from_gequbao(name):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://www.gequbao.com/")
        input1 = page.locator("#s-input")
        input1.fill(name)
        button1 = page.locator("#s-btn")
        button1.click()
        button2 = page.get_by_text("播放&下载").first
        button2.click()
        button3 = page.locator('#btn-download-mp3')
        button3.click()
        try:
            button4 = page.get_by_text("下载低品质MP3").first
            button4.click()
        except:
            pass
        download_click(page, name, 831, 512, 786, 505)
        browser.close()
        time.sleep(5)


def steal_music_from_yeyulingfeng(name_list):  # ver:1.0.0
    def new_download(browser, name):
        page = browser.new_page()
        page.goto("https://www.yeyulingfeng.com/tools/music/?name=" + name + " " + author + "&type=netease")
        page.set_viewport_size({"width": 1024, "height": 768})
        # input1 = page.locator("#input")
        # input1.fill(name)
        button1 = page.locator("#j-src-btn")
        button1.click()
        page.wait_for_load_state("load")
        download_click(page, name, 832, 515, 797, 464)
        time.sleep(2)

    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome", headless=False)
        context = browser.new_context(no_viewport=True)
        time.sleep(5)
        for name in name_list:
            new_download(browser, name)
        browser.close()


'''
with sync_playwright() as p:
    browser = p.chromium.launch(channel="chrome", headless=False, args=['--start-maximized'])
    page = browser.new_page()
    context = browser.new_context(no_viewport=True)
    page.goto("https://sy-sycdn.kuwo.cn/4120db271569429926bb9795b70399f2/66d410b2/resource/n2/70/55/756351052.mp3?bitrate$128&from=vip")
    download_click(page, "test", 835, 534, 807, 488)
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
        #print(len(name))
        print(name[i])
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
        print('step:', step)
    return name_list


need_format_name = input('name:')
author = input('author:')
name_list = name_format(need_format_name)
print(name_list)
steal_music_from_yeyulingfeng(name_list)


# <ul class="f-hide"><li><a href="/song?id=1335796886">花间游</a></li><li><a href="/song?id=487864613">寂川</a></li><li><a href="/song?id=1352004027">得似旧时</a></li><li><a href="/song?id=428391474">那年夏天，阳光正好</a></li><li><a href="/song?id=1483533107">薄荷绿</a></li><li><a href="/song?id=1808372495">晴云</a></li><li><a href="/song?id=1860122134">荒川之月</a></li><li><a href="/song?id=2075085097">薰风初昼长</a></li><li><a href="/song?id=515715891">In The Good Times</a></li><li><a href="/song?id=460173322">观灯</a></li><li><a href="/song?id=1300726769">旧事</a></li><li><a href="/song?id=2056529061">再次回到那个夏天</a></li><li><a href="/song?id=1341851239">雪满山中</a></li><li><a href="/song?id=2123300735">没有结局的开始</a></li><li><a href="/song?id=2084455740">须臾之梦</a></li><li><a href="/song?id=1825216246">远书</a></li><li><a href="/song?id=410714365">清月</a></li><li><a href="/song?id=2622641914">凌晨三点的寂静群山</a></li><li><a href="/song?id=1993440849">醒来明月，醉时清风</a></li><li><a href="/song?id=1444647128">我能想到的最幸福的事</a></li><li><a href="/song?id=487866745">暮落（终章）</a></li><li><a href="/song?id=1294799290">夏风微凉</a></li><li><a href="/song?id=1454884913">人间风景</a></li><li><a href="/song?id=1971658643">甜味夏天</a></li><li><a href="/song?id=542818195">回忆之末</a></li><li><a href="/song?id=404459371">浮游于梦</a></li><li><a href="/song?id=1444639931">风中有音</a></li><li><a href="/song?id=1365858944">山桃如雪</a></li><li><a href="/song?id=487866133">朝生（序章）</a></li><li><a href="/song?id=1498649082">一人之境</a></li><li><a href="/song?id=2146742860">黎明到来之前</a></li><li><a href="/song?id=2035130279">她和她的她</a></li><li><a href="/song?id=428387405">以道入魔</a></li><li><a href="/song?id=487864776">雾原</a></li><li><a href="/song?id=864892593">时间飞行 钢琴版</a></li><li><a href="/song?id=556036685">向着朝阳，我走过冬夜寒风</a></li><li><a href="/song?id=1358343231">浮生(inst.)</a></li><li><a href="/song?id=1380302367">流萤</a></li><li><a href="/song?id=487866627">崖居</a></li><li><a href="/song?id=404460258">归风</a></li><li><a href="/song?id=404460260">明镜亦非台</a></li><li><a href="/song?id=515716756">If The Story Ends Well</a></li><li><a href="/song?id=1874430113">梦归</a></li><li><a href="/song?id=2112799613">相逢于时光彼岸</a></li><li><a href="/song?id=2132050270">深海消亡前的诗</a></li><li><a href="/song?id=502569500">破晓</a></li><li><a href="/song?id=1927459179">东池宴</a></li><li><a href="/song?id=1406665130">花开有时</a></li><li><a href="/song?id=1904805030">逆着风</a></li><li><a href="/song?id=409650937">one day the miracle will come</a></li></ul>
