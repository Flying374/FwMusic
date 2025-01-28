# Author: Flying374
# Version: 1.2.1-pre3
# How to prove that I am existing?
import LocalAPI_v10201_p3 as LocalAPI
# import tkinter as tk
# import ttkbootstrap as ttk
# from ttkbootstrap.constants import *
from ttkbootstrap import Style
from ttkbootstrap.dialogs import *
import threading
import time

Supported_api_version = 'v10201_p3'
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


def download_music(artist_id, type):
    artist = LocalAPI.Artist(artist_id)
    artist.get_details(meter_num1)
    download_numbers.set_value(len(artist.get_songs()))
    artist.download(type, meter_num2)
    artist.save(True)


def download_music_thread():
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


# Main Window
root = ttk.Window(title="FwMusic v1.2.1-pre3", themename="minty", size=(500, 350), minsize=(500, 350),
                  maxsize=(500, 350), iconphoto=, resizable=(False, False),)
root.place_window_center()
variable_value = ttk.StringVar(root)


# About Menu
def FwMusic_about():
    Messagebox.okcancel(title='About FwMusic', message='FwMusic is a simple music downloader.'
                                                       '\nThis product is for learning purposes only.\nWe are not '
                                                       'responsible for any consequences resulting from the use of '
                                                       'this product.\nVersion:'
                                                       '1.2.1-pre3\nAuthor: Flying374.\nFor more '
                                                       'information, please visit: '
                                                       'https://github.com/Flying374/FwMusic.')


def Author_about():
    Messagebox.okcancel(title='About Author', message='Flying374 is a student with poor grade.\n'
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
label1.place(relx=0.35, rely=0.09, anchor=CENTER)
label2 = ttk.Label(root, text="v.1.2.1-pre3", font=('georgia', 20), bootstyle=PRIMARY)
label2.place(relx=0.67, rely=0.14, anchor=CENTER)

# Search Bar& Button
search_bar = ttk.Entry(root, width=50, font=('georgia', 14), bootstyle=INFO)
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
                   subtextstyle="warning", interactive=False,
                   bootstyle='primary', )
meter1.place(relx=0.25, rely=0.68, anchor=CENTER)
meter2 = ttk.Meter(metertype="full", metersize=180, padding=50, amounttotal=download_numbers.get_value(),
                   subtext="Downloading...",
                   subtextstyle="warning", interactive=False,
                   bootstyle='primary', )
meter2.place(relx=0.75, rely=0.68, anchor=CENTER)


def meter_upgrade():
    while True:
        meter1.configure(amountused=meter_num1.get_value())
        meter2.configure(amountused=meter_num2.get_value())
        meter2.configure(amounttotal=download_numbers.get_value())
        #  print(meter_num1.get_value(), meter_num2.get_value(), download_numbers.get_value())  # debug
        time.sleep(0.01)


thread1 = threading.Thread(target=meter_upgrade)
thread1.start()

root.mainloop()
