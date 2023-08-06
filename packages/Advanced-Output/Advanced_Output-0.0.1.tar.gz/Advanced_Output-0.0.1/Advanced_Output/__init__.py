#主文件
#导入模块
from tkinter import *
import pygame
from PIL import Image,ImageTk
import turtle
import random
#显示图片的函数
def showImage(path):
    window=Tk()
    load = Image.open(path)
    wid = str(load.width)
    hei = str(load.height)
    window.resizable(width=False, height=False)
    window.geometry(wid+'x'+hei)
    window.title(path)
    render= ImageTk.PhotoImage(load)
    img = Label(window,image=render)
    img.image = render
    img.place(x=0,y=0)
    window.mainloop()
#播放音乐
def playMusic(path):
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(path)
    pygame.mixer.music.play()
#折线模拟运行
def lineSimulation(derec_list):
    for lister in derec_list:
        dlc()
        turtle.goto(lister[0],lister[1])
    dlc()
    turtle.done()
#画圆（引用于折线模拟）
def dlc():
    turtle.begin_fill()
    turtle.fillcolor("red")
    turtle.circle(2)
    turtle.end_fill()
#main
def main():
    path = input("路径？")
    try:
        playMusic(path)
        lineSimulation([[0,0],[100,20],[200,-10]])
    except:
        print("啊额，出错啦！")
if __name__ == "__main__":
    main()
