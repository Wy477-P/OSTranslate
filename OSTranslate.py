import tkinter as tk
from tkinter import ttk
import os
import easyocr
import PIL.ImageGrab
import hashlib
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

root = tk.Tk()
root.attributes("-topmost", True)
root.configure(background="black")
root.overrideredirect(True)
root.resizable(True, True)
root.geometry("600x335")


bar = tk.Frame(root, bg="black", height=16)
def start_move(event):
    root.x = event.x
    root.y = event.y
def stop_move(event):
    root.x = None
    root.y = None
def on_motion(event):
    deltax = event.x - root.x
    deltay = event.y - root.y
    x = root.winfo_x() + deltax
    y = root.winfo_y() + deltay
    root.geometry("+%s+%s" % (x, y))
bar.bind("<ButtonPress-1>", start_move)
bar.bind("<ButtonRelease-1>", stop_move)
bar.bind("<B1-Motion>", on_motion)

title = tk.Label(bar, text="OSTranslate v1.0", fg="white", bg="black", borderwidth=1)

exit = tk.Canvas(bar, width=15, height=15, highlightthickness=0, bg="black", borderwidth=1)
exit.create_line(0, 0, 15, 15, fill="white")
exit.create_line(0, 15, 15, 0, fill="white")
def on_enter(event):
    exit.config(bg="#ff0000")
def on_leave(event):
    exit.config(bg="black")
def on_press(event):
    exit.config(bg="#8B0000")
def on_release(event):
    exit.config(bg="red")
    os._exit(0)
exit.bind("<Enter>", on_enter)
exit.bind("<Leave>", on_leave)
exit.bind("<ButtonPress-1>", on_press)
exit.bind("<ButtonRelease-1>", on_release)


output = tk.Text(root, wrap=tk.WORD, state="disabled", borderwidth=0, bg="#333333", fg="white")
def po(text):
    output.config(state="normal")
    output.delete(1.0, tk.END)
    output.insert(tk.END, text)
    output.config(state="disabled")
    output.see(tk.END)

key = tk.Entry(root, borderwidth=0, bg="#333333", fg="white")
outlang = tk.Entry(root, borderwidth=0, bg="#333333", fg="white")
inlang = tk.Entry(root, borderwidth=0, bg="#333333", fg="white")
to = tk.Text(root, state="normal", borderwidth=0, bg="black", fg="white")
tclass = tk.Entry(root, borderwidth=0, bg="#333333", fg="white")

bar.pack(fill=tk.X)
title.place(x=0, y=0)
exit.place(x=585, y=0)
output.place(x=15, y=30, width=570, height=255)  
key.place(x=15, y=300, width=430, height=20)
outlang.place(x=545, y=300, width=40, height=20)
inlang.place(x=510, y=300, width=15, height=20)
to.place(x=525, y=300, width=20, height=20)
to.insert(tk.END, "->")
to.config(state="disabled")
tclass.place(x=455, y=300, width=45, height=20)

def image_hash(image):
    image_bytes = image.tobytes()
    return hashlib.md5(image_bytes).hexdigest()

old_hash = None
def translate():
    global old_hash
    img = PIL.ImageGrab.grabclipboard()
    if img is None:
        po("No image found in clipboard. Use snipping tool to copy an image with text in input language to continue.")
    else:
        current_hash = image_hash(img)
        if current_hash != old_hash:
            try:
                img_array = np.array(img)
                reader = easyocr.Reader([inlang.get()])
                etext = reader.readtext(img_array)
                text = ' '.join([item[1] for item in etext])
                try:
                    link = key.get()
                    olang = outlang.get()
                    ilang = inlang.get()
                    link = link.format(inlang=ilang, outlang=olang, text=text)
                    options = webdriver.ChromeOptions()
                    options.add_argument('--headless')
                    options.add_argument('--disable-gpu')
                    driver = webdriver.Chrome(options=options)
                    driver.get(link)
                    wait = WebDriverWait(driver, 10)
                    translated_span = wait.until(
                    EC.presence_of_element_located((By.CLASS_NAME, tclass.get()))
                    )
                    result = translated_span.text
                    print(link)
                    driver.quit()
                    po(result)
                except Exception as e:
                    po(f"Translation Failed. See here: {e}" + "\n" + "Detected text:" + text)
            except Exception as e:
                po(f"OCR Failed. See here: {e}")
            old_hash = current_hash
            
def loop():
    translate()
    root.after(1000, loop)
root.after(1000, loop)

key.insert(0, "https://translate.google.com/?sl=auto&tl={outlang}&text={text}&op=translate")
outlang.insert(0, "en")
inlang.insert(0, "ja")
tclass.insert(0, "ryNqvb")
root.mainloop()

