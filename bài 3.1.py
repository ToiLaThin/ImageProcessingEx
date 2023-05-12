import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image
from tkinter import filedialog
import os
import numpy as np

root = Tk()
root.geometry("550x300+300+150")
root.resizable(width=True, height=True)
root.img = None
root.R =tk.StringVar()
root.G =tk.StringVar()
root.B =tk.StringVar()
#Find image
def openfn():
    filename = filedialog.askopenfilename(title='Open')
    return filename

#Here's where we load the image
def open_img():
    x = openfn()
    img = Image.open(x)
    root.img = img
    img1 = img.resize((250, 250), Image.ANTIALIAS)
    img1 = ImageTk.PhotoImage(img1)
    panel = Label(root, image=img1)
    panel.image = img1
    panel.grid(column=0,row=2,columnspan = 2)

def change_color(r=0,g=0,b=0):
    img = root.img.convert("RGB")
    datas = img.getdata()
    print(datas[1])
    print(type(datas))
    new_image_data = []

    for item in datas:
        # change all white (also shades of whites) pixels to yellow
        if item[0] in list(range(0, 255)):
            new_image_data.append((r, g, b))
        else:
            new_image_data.append(item)
    img.putdata(new_image_data)
    return img

def update_color():

    r = int(root.R.get())
    g = int(root.G.get())
    b = int(root.B.get())
    img2 = change_color(r,g,b)
    img2 = img2.resize((250, 250), Image.ANTIALIAS)
    img2 = ImageTk.PhotoImage(img2)
    panel2 = Label(root, image=img2)
    panel2.image = img2
    panel2.grid(column=2,row=2,columnspan = 2)
#My attempt for gray filter but reloading an image
    
#buttons
btn = tk.Button(root, text='Select an image', command=open_img).grid(column=0,row=0)
#input
R = tk.Entry(root,textvariable=root.R).grid(column=0,row=1)
G = tk.Entry(root,textvariable=root.G).grid(column=1,row=1)
B = tk.Entry(root,textvariable=root.B).grid(column=2,row=1)
btn = tk.Button(root, text='UpdateRGB', command=update_color).grid(column=3,row=1)
root.mainloop()