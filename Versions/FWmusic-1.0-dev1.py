from playwright.sync_api import sync_playwright
import time
import pyautogui


def download(page, name):
    show = page.locator('#div')
    show.click()
    with page.expect_download() as download_info:
        download_btn = page.get_by_text("下载").first
        download_btn.click()
        download = download_info.value
        download.save_as(name + ".mp3")


def download_click(page, name, x_1, y_1, x_2, y_2):
    with page.expect_download() as download_info:
        pyautogui.click(x_1, y_1)
        time.sleep(1)
        pyautogui.click(x_2, y_2)
        download = download_info.value
        download.save_as(name + ".mp3")


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
        download_click(page, name, 835, 534, 807, 488)
        browser.close()
        time.sleep(5)


def steal_music_from_yeyulingfeng(name_list):
    def new_download(browser, name):
        page = browser.new_page()
        page.goto("https://www.yeyulingfeng.com/tools/music/?name=" + name + " " + author + "&type=netease")
        # input1 = page.locator("#input")
        # input1.fill(name)
        button1 = page.locator("#j-src-btn")
        button1.click()
        page.wait_for_load_state("load")
        download_click(page, name, 835, 534, 807, 488)
        time.sleep(2)

    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome", headless=False, args=['--start-maximized'])
        context = browser.new_context(no_viewport=True)
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


def name_format(name):
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


need_format_name = input('name:')
author = input('author:')
name_list = name_format(need_format_name)
print(name_list)
steal_music_from_yeyulingfeng(name_list)