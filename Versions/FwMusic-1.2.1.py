# Author: Flying374
# Version: 1.2.1
# How to prove that I am existing?

import os.path
import LocalAPI_v10201 as LocalAPI
from ttkbootstrap.dialogs import *
import threading
import time
import pygame
import random

Supported_api_version = 'v10201'
Api = LocalAPI.API()

if Api.get_version() != Supported_api_version:
    print("ErrA1 : LocalAPI Version doesn't match Program version.")
    print('Now the version is :' + Api.get_version() + '.')
    print('Please use :' + Supported_api_version + '.')
    exit()

Errinfo = LocalAPI.ErrInfo()
Flog = LocalAPI.FLog()
Flog.create()

meter_num1 = LocalAPI.GlobalVar()
meter_num2 = LocalAPI.GlobalVar()
download_numbers = LocalAPI.GlobalVar()

meter_num1.set_value(0)
meter_num2.set_value(0)
download_numbers.set_value(1)


# Main Window
root = ttk.Window(title="FwMusic v1.2.1", themename="minty", size=(500, 350), minsize=(500, 350),
                  maxsize=(500, 350))
root.place_window_center()
'''
image = ttk.PhotoImage(file='bg.gif')
background_label = ttk.Label(root, image=image)
background_label.place(relx=0.5, rely=0.5, anchor='center')
'''


variable_value = ttk.StringVar(root)
variable_value.set('0')
variable_music = ttk.BooleanVar(root)
variable_music_play = ttk.StringVar(root)
variable_music_play.set("Background Music : Off")
variable_state_meter1 = ttk.StringVar(root)
variable_state_meter2 = ttk.StringVar(root)
variable_state_meter1_text = ttk.StringVar(root)
variable_state_meter2_text = ttk.StringVar(root)
variable_state_meter1.set("dark")
variable_state_meter2.set("dark")
variable_state_meter1_text.set("dark")
variable_state_meter2_text.set("dark")


def download_music_thread():
    def download_music(artist_id, type):
        variable_state_meter1.set("warning")
        variable_state_meter1_text.set("warning")
        artist = LocalAPI.Artist(artist_id)
        if artist.get_details(meter_num1) != 'ErrG1':
            variable_state_meter1.set("success")
            variable_state_meter1_text.set("success")
            variable_state_meter2.set("warning")
            variable_state_meter2_text.set("warning")
            download_numbers.set_value(len(artist.read(type))+1)
            if artist.download(type, meter_num2) != 'ErrAD1':
                artist.save(True)
                variable_state_meter2.set("success")
                variable_state_meter2_text.set("success")
                meter_num2.add_value(1, 0.1)
                Messagebox.show_info(title='Success', message='Download completed.')
            else:
                variable_state_meter2.set("danger")
                variable_state_meter2_text.set("danger")
                Messagebox.show_error(title='Error', message='Download failed.')
        else:
            variable_state_meter1.set("danger")
            variable_state_meter2.set("danger")
            variable_state_meter1_text.set("danger")
            variable_state_meter2_text.set("danger")
            Messagebox.show_error(title='Error', message='Analysis failed.')
    artist_id = search_bar.get()
    value_list = ['latest', 'new', 'old']
    type = value_list[int(variable_value.get())]
    if artist_id != '' and type != '':
        t1 = threading.Thread(target=download_music, args=(artist_id, type))
        t1.start()


def clear():
    search_bar.delete(0, 'end')
    variable_value.set('0')
    meter_num1.set_value(0)
    meter_num2.set_value(0)
    download_numbers.set_value(1)
    variable_state_meter1.set("dark")
    variable_state_meter2.set("dark")
    variable_state_meter1_text.set("dark")
    variable_state_meter2_text.set("dark")


# music
def backgroud_music():
    state_last = False
    while True:
        state = variable_music.get()
        music_list = ['乌云石远行.mp3', 'Asphyxia.mp3', 'ИIАЯ.mp3', 'The End.mp3', '向晚之诗 吉他版.mp3', '夏の喚く.mp3',
                      '无已恋君时.mp3', '樱花七日.mp3', '樱花雨.mp3', '葬花.mp3', '远空，追寻与相遇.mp3', '雪满山中.mp3',
                      '鸢尾花の夏梦.mp3']

        if state and not state_last:
            num = random.randint(0, 12)
            pygame.mixer.music.load(os.path.join('BGM', music_list[num]))  # 加载声音文件
            variable_music_play.set("Background Music :" + music_list[num][:-4])
            pygame.mixer.music.play()
            # print(2)
        if state and pygame.mixer.music.get_busy() == False:
            num = random.randint(0, 12)
            pygame.mixer.music.load(os.path.join('BGM', music_list[num]))  # 加载声音文件
            variable_music_play.set("Background Music :" + music_list[num][:-4])
            pygame.mixer.music.play()
        if not state:
            pygame.mixer.music.stop()
            variable_music_play.set("Background Music : Off")
        time.sleep(0.1)
        # print(1)
        state_last = state

pygame.mixer.init()
tm1 = threading.Thread(target=backgroud_music)
tm1.start()

# About Menu
def FwMusic_about():
    Messagebox.okcancel(title='About FwMusic', message='FwMusic is a simple music downloader.'
                                                       '\nThis product is for learning purposes only.\nWe are not '
                                                       'responsible for any consequences resulting from the use of '
                                                       'this product.\nVersion:'
                                                       '1.2.1\nAuthor: Flying374.\nFor more '
                                                       'information, please visit: '
                                                       'https://github.com/Flying374/FwMusic.')


def Author_about():
    Messagebox.okcancel(title='About Me', message='Flying374 is a Fw with poor grade.\n'
                                                  'Mail: doorofthevoid@qq.com\n'
                                                  'For more information, please visit: '
                                                  'https://github.com/Flying374.')


menubar = ttk.Menu(root)
filemenu = ttk.Menu(menubar)
about = ttk.Menu(menubar, tearoff=0)
menubar.add_cascade(label='About', menu=about)
about.add_command(label='About FwMusic', command=FwMusic_about)
about.add_command(label='About Me', command=Author_about)
root.config(menu=menubar)

# Main Label
label1 = ttk.Label(root, text="FwMusic", font=('georgia', 50), bootstyle=PRIMARY)

label1.place(relx=0.44, rely=0.09, anchor=CENTER)
label2 = ttk.Label(root, text="v.1.2.1", font=('georgia', 20), bootstyle=PRIMARY)
label2.place(relx=0.71, rely=0.14, anchor=CENTER)

# Search Bar& Button
search_bar = ttk.Entry(root, width=50, font=('georgia', 14), bootstyle=SUCCESS)
search_bar.place(relx=0.48, rely=0.22, anchor=CENTER)
search_button = ttk.Button(root, text="Get", command=download_music_thread,
                           bootstyle=SUCCESS)
search_button.place(relx=0.93, rely=0.22, anchor=CENTER)

select_label = ttk.Label(root, text="Type:", font=('georgia', 14), bootstyle=INFO)
select_label.place(relx=0.05, rely=0.31, anchor=CENTER)
select_button1 = ttk.Radiobutton(root, text="latest", value=0, variable=variable_value, bootstyle=PRIMARY)
select_button1.place(relx=0.2, rely=0.31, anchor=CENTER)
select_button2 = ttk.Radiobutton(root, text="new", value=1, variable=variable_value, bootstyle=PRIMARY)
select_button2.place(relx=0.4, rely=0.31, anchor=CENTER)
select_button3 = ttk.Radiobutton(root, text="old", value=2, variable=variable_value, bootstyle=PRIMARY)
select_button3.place(relx=0.6, rely=0.31, anchor=CENTER)

# meter
meter1 = ttk.Meter(metertype="full", metersize=180, padding=50, amounttotal=100, subtext="Analysising...",
                   subtextstyle="dark", interactive=False,
                   bootstyle='dark', )
meter1.place(relx=0.25, rely=0.68, anchor=CENTER)
meter2 = ttk.Meter(metertype="full", metersize=180, padding=50, amounttotal=download_numbers.get_value(),
                   subtext="Downloading...",
                   subtextstyle="dark", interactive=False,
                   bootstyle='dark', )
meter2.place(relx=0.75, rely=0.68, anchor=CENTER)

# clear button
clear_button = ttk.Button(root, text="Clear", command=clear, bootstyle=DANGER)
clear_button.place(relx=0.48, rely=0.8, anchor=CENTER)


def eexit():
    mb = Messagebox.okcancel(title='Exit', message='Are you sure to exit?')
    # print(mb)
    if mb == 'OK':
        os._exit(0)


# background music thread
play_button = ttk.Checkbutton(root, text="Music", variable=variable_music, bootstyle="round-toggle")
play_button.place(relx=0.09, rely=0.89, anchor=CENTER)
label3 = ttk.Label(root, text='Background Music : Off', font=('georgia', 14), bootstyle=PRIMARY)
label3.place(relx=0.02, rely=0.95, anchor=W)

# Exit Button
exit_button = ttk.Button(root, text="Exit", command=eexit, bootstyle=DANGER)
exit_button.place(relx=0.95, rely=0.95, anchor=CENTER)


def main_upgrade():
    while True:
        meter1.configure(amountused=meter_num1.get_value(), bootstyle=variable_state_meter1.get(),
                         subtextstyle=variable_state_meter1_text.get())
        meter2.configure(amountused=meter_num2.get_value(), bootstyle=variable_state_meter2.get(),
                         subtextstyle=variable_state_meter2_text.get())
        meter2.configure(amounttotal=download_numbers.get_value())
        label3.configure(text=variable_music_play.get()) 
        time.sleep(0.01)
        try:
            if search_bar.get() != '':
                int(search_bar.get())
                search_bar.configure(bootstyle=SUCCESS)
        except Exception:
            search_bar.configure(bootstyle=WARNING)


thread1 = threading.Thread(target=main_upgrade)
thread1.start()

root.mainloop()
