import webbrowser
from gtts import *
from tkinter import *
from tkinter.ttk import *
from tkinter import Label as Linklabel
from tkinter import messagebox
from tkinter import filedialog
from pygame import mixer
import datetime
import os
import pyttsx3
import threading
import time
import sys
import subprocess


def select_file():
    filetypes = (
        ('Text files', '*.txt'),
        ('All files', '*.*')
    )
    filename = filedialog.askopenfilename(
        title='Open text file',
        initialdir='/',
        filetypes=filetypes)
    with open(filename, 'r') as f:
        contents = f.read()
    text.delete('1.0', END)
    text.insert('end', contents)


def save_file():
    filename = filedialog.asksaveasfilename(initialdir='/', title='Save text file',
                                            filetypes=(('Text files', '*.txt'), ('All Files', '*.*')), defaultextension=".txt")
    final_file = open(filename, "w+")
    final_file.write(text.get(1.0, 'end-1c'))


def check_for_google_protocol():
    while True:
        if protocol.get() == "Google":
            rate.current(1)
            rate.config(state='disabled')
            language.config(state="readonly")
            time.sleep(0.1)
        else:
            rate.config(state='readonly')
            language.current(0)
            language.config(state="disabled")
            time.sleep(0.1)

def language_check():
    if protocol.get() != "Google":
        language.config(state='disabled')
    else:
        language.config(state='readonly')

def make_output():

    def ms_voices_protocol():
        start.config(state='disabled')
        if protocol.get() == "Microsoft Zira":
            engine = pyttsx3.init()
            if rate.get() == "Fastest":
                engine.setProperty('rate', 160)
            elif rate.get() == "Normal":
                engine.setProperty('rate', 135)
            else:
                engine.setProperty('rate', 100)
            voices = engine.getProperty('voices')
            engine.setProperty('voice', voices[1].id)
            engine.say(input_words)
            engine.runAndWait()
            start.config(state='normal')
        elif protocol.get() == "Microsoft David":
            engine = pyttsx3.init()
            if rate.get() == "Fastest":
                engine.setProperty('rate', 160)
            elif rate.get() == "Normal":
                engine.setProperty('rate', 135)
            else:
                engine.setProperty('rate', 100)
            voices = engine.getProperty('voices')
            engine.setProperty('voice', voices[0].id)
            engine.say(text.get(1.0, 'end-1c'))
            engine.runAndWait()
            start.config(state='normal')

    input_words = text.get(1.0, "end-1c")
    if language.get() == "English":   # "English", "Español", "Português", "Français", "普通话"
        lang_code = "en"
    elif language.get() == "Español":
        lang_code = "es"
    elif language.get() == "Português":
        lang_code = "pt"
    elif language.get() == "Français":
        lang_code = "fr"
    elif language.get() == "русский":
        lang_code = "ru"
    else:
        lang_code = "zh-CN"
    if protocol.get() == "Google":
        current_time = datetime.datetime.now().strftime("%Y_%m_%d-%I-%M-%S_%p")
        tts = gTTS(input_words, lang=lang_code)
        tts.save(str(current_time + ".mp3"))
        mixer.init()
        mixer.music.load(current_time + ".mp3")
        mixer.music.play()
        return

    background2 = threading.Thread(
        name='background', target=lambda: ms_voices_protocol())
    background2.daemon = True
    background2.start()


def clean_up():
    try:
        mixer.music.unload()
    except:
        pass

    if messagebox.askokcancel("Quit", "Do you want to quit EasyTTS?"):
        win1.destroy()
        directory = "./"
        files_in_directory = os.listdir(directory)
        filtered_files = [
            file for file in files_in_directory if file.endswith(".mp3")]
        for file in filtered_files:
            path_to_file = os.path.join(directory, file)
            os.remove(path_to_file)
        sys.exit()


def language_check(index, value, op):
    if protocol.get() == "Google":
        rate.current(1)
        rate.config(state='disabled')
        language.config(state="readonly")
        time.sleep(0.1)
    else:
        rate.config(state='readonly')
        language.current(0)
        language.config(state="disabled")
        time.sleep(0.1)
        

def get_help():


    def close_help_window():
        win2.destroy()
        help_button.config(state="normal")


    def callback(url):
        webbrowser.open_new_tab(url)
    help_button.config(state="disabled")
    win2 = Tk()
    win2.geometry("1000x550")
    win2.iconbitmap("speechico2.ico")
    win2.title("How to use/Credits")
    win2.protocol("WM_DELETE_WINDOW", close_help_window)
    
    win2.rowconfigure(1, weight=5)
    win2.columnconfigure(1, weight=5)

    with open("howto.txt", 'r') as h:
        instructions = h.read()
    helper = Text(win2, font='DejaVu', wrap='word', relief='solid')
    helper.grid(row=1, column=1, padx=2, pady=2, sticky='nsew')

        
    scrollbar2 = Scrollbar(win2, orient='vertical', command=helper.yview)
    scrollbar2.grid(row=1, column=2, sticky='ns')

    helper['yscrollcommand'] = scrollbar2.set

    helper.insert('end', instructions)
    helper.config(state='disabled')

    close_window = Button(win2, text="Close", command=close_help_window)
    close_window.grid(row=2, column=1, pady=10, sticky='ns')

    link = Linklabel(
        win2, text="Need support or have a feature idea?", cursor="hand2", fg="blue")
    link.grid(row=3, column=1, padx=5, sticky='ns')
    link.bind("<Button-1>", lambda e:
              callback("https://sourceforge.net/p/easytts/tickets/new/"))

    win2.mainloop()


try:
    check = subprocess.check_output("ping google.com", shell=True)
    protocol_list = ["Google", "Microsoft David", "Microsoft Zira"]
except subprocess.CalledProcessError:
    messagebox.showinfo(
        "EasyTTS", "You can't use the Google TTS protocol because you aren't connected to the Internet or another error occured.")
    protocol_list = ["Microsoft David", "Microsoft Zira"]

win1 = Tk()
win1.geometry("600x430")
win1.title("EasyTTS")
win1.iconbitmap("speechico2.ico")
win1.columnconfigure(1, weight=10000)
win1.rowconfigure(1, weight=10000)
win1.rowconfigure(2, weight=10)
win1.protocol("WM_DELETE_WINDOW", lambda: clean_up())


text = Text(win1, width=60, height=14, font='arial',
            relief='solid', wrap='word')
text.grid(row=1, column=1, padx=5, pady=5, sticky='nsew')

scrollbar = Scrollbar(win1, orient='vertical', command=text.yview)
scrollbar.grid(row=1, column=2, sticky='ns')

text['yscrollcommand'] = scrollbar.set

start = Button(win1, text='Play', command=lambda: make_output())
start.grid(row=2, column=1, padx=5, pady=5, sticky='nw')

help_button = Button(win1, text="How to use", command=lambda: get_help())
help_button.grid(row=2, column=1, padx=5, pady=5, sticky='ne', columnspan=2)
settings = LabelFrame(win1, text="TTS voice, voice rate, language")
settings.grid(row=2, column=1, pady=5, sticky='n', rowspan=2)

language = Combobox(settings, values=[
                    "English", "Español", "Português", "Français", "русский", "普通话"], state="readonly")
language.current(0)
language.grid(row=4, column=1, sticky='n')

rate = Combobox(settings, values=["Fastest",
                "Normal", "Slowest"], state='readonly')
rate.current(1)
rate.grid(row=3, column=1, pady=3, sticky='n')

string_var = StringVar()
string_var.trace('w', language_check)

protocol = Combobox(settings, values=protocol_list, textvar=string_var, state='readonly')
protocol.current(0)
protocol.grid(row=2, column=1, sticky='n')


open_file = Button(win1, text='Open text file', command=lambda: select_file())
open_file.grid(row=3, column=1, padx=5, sticky='nw')

save = Button(win1, text='Save as text file', command=lambda: save_file())
save.grid(row=3, column=1, padx=5, pady=5, sticky='ne', columnspan=2)

win1.mainloop()
