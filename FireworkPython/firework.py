"""
@author:Alex Chen
Bilibili用户名:空指针解引用
"""
import random
from numpy import sin, cos, pi, linspace
from tkinter import *
from PIL import Image, ImageTk
from time import sleep
CANVAS_WIDTH = 800   # 画布的宽
CANVAS_HEIGHT = 600  # 画布的高
CANVAS_CENTER_X = CANVAS_WIDTH / 2  # 画布中心的X轴坐标
CANVAS_CENTER_Y = CANVAS_HEIGHT / 2  # 画布中心的Y轴坐标
IMAGE_ENLARGE = 8   # 放大比例
SINGLE_NUM = 6      # 每个周期烟花的个数
LAUNCH_LENGTH = 30     # 发射运动周期
EXP_CIRCLE = 10
COLOR_CHOOSE = random.randint(0,5)

# 通过改变这个值可以改变程序运行速度

CYCLE = 5

#################

COLORS = ["pink","skyblue","gold","palegreen","moccasin","violet"] # 烟花的颜色
LAUNCH_COLOR = "silver"

def get_img(filename, width, height):
    im = Image.open(filename).resize((width, height))
    im = ImageTk.PhotoImage(im)
    return im   

def norm2can( y ):
    return CANVAS_HEIGHT-y
def launch_function(x, y, velo, angle):
    """
    发射生成函数
    """ 
    # print("launch_start pos = (%.6f,%.6f)"%(x,y))
    next_x = x + velo*cos(angle)
    next_y = y + velo*sin(angle)
    # print("launch_end pos = (%.6f,%.6f)"%(next_x,next_y))
    return next_x, next_y

def circle_function(t, a, b, radius):
    """
    生成圆函数
    """
    length = 4
    # 单位圆
    # x=cos(t) 
    # y=sin(t)
    # 放大
    x  = cos(t) * radius
    y  = sin(t) * radius
    x1 = cos(t) * (radius + length)
    y1 = sin(t) * (radius + length)
    # 移到画布中央并进行偏移
    # x += CANVAS_CENTER_X + a
    # y += CANVAS_CENTER_Y + b
    x  += a
    y  += b
    x1 += a
    y1 += b
    return int(x), int(y),int(x1),int(y1)

def explode (color_num ) :
    return 0

class Firework:
    def __init__(self) :
        self.dots_pos = []
        self.wait = random.randint(30,60)
        self.produce()
    def produce(self):
        for fr in range(SINGLE_NUM): # 一个周期里烟花的数目
            print("len(self.dots_pos)1 = ",len(self.dots_pos))
            color_mod  = random.randint(0,2)
            color = COLORS[fr]
            # 前 LAUNCH_LENGTH 为发射周期
            velo = random.randint(8,12) # 烟花的发射速度
            angle = random.uniform((pi/3),(2*pi/3)) 
            x = CANVAS_CENTER_X
            y = 120
            
            for lc in range(LAUNCH_LENGTH): # 一个烟花的发射过程
                next_x ,next_y = launch_function(x,y,velo,angle) 
                self.dots_pos.append([[x,y,next_x,next_y,2,LAUNCH_COLOR]])
                x = next_x
                y = next_y
            print("len(self.dots_pos)2 = ",len(self.dots_pos))
            # 以后为爆炸周期
            exp_x = x
            exp_y = y
            start_angles =[]
            start_colors = []
            random_angles = list(linspace(0,2*pi,240))
            len_angle = len(random_angles)
            random.shuffle(random_angles)
            n_layer = 24
            every_layer = int(240/24)
            for i in range(n_layer):
                start_colors.append([ COLORS[random.randint(0,5)] for j in range(every_layer)])
                start_angles.append(random_angles[int(len_angle*(i/n_layer)):int(len_angle*((i+1)/n_layer))])
            dis = [0 for layer in range(n_layer) ]
            velo = 3
            for layer in range(n_layer):
                for step in range(2):
                    group=[]
                    step_color = COLORS[random.randint(0,5)]
                    for single in range(layer+1):       # 每一次
                        angles = start_angles[single]
                        single_pos = [list(circle_function(angle,exp_x,exp_y,dis[single])) for angle in angles]
                        for loc in range(len(single_pos)):
                            if color_mod == 0:
                                # 彩色
                                single_pos[loc].append(start_colors[single][loc])
                            elif color_mod == 1:
                                # 单色
                                single_pos[loc].append(color)
                            elif color_mod == 2:
                                # 圈层彩色
                                single_pos[loc].append(step_color)
                        group.extend(single_pos)
                        dis[single] += velo #[layer] 
                    self.dots_pos.append(group)

                        

    def render(self, canvas, iterator,ids):  
        for id in ids:
            canvas.delete(id)
        iterator = iterator% (468+self.wait)        # 6*(40+3*24) = 552
        rets = []
        if iterator <= self.wait:
            sleep(0.00001)
            return rets
        else:
            iterator -= self.wait
        if iterator%78 < 30:
            for group in self.dots_pos[iterator]:
                # print("launch")
                # print("group = ",group)
                ret = canvas.create_line(group[0],norm2can(group[1]),group[2],norm2can(group[3]),width = 2, fill=LAUNCH_COLOR)
                rets.append(ret)
        else:
            for group in self.dots_pos[iterator]:
                # print("explode")
                # print("group = ",group)
                # canvas.create_oval(group[0],norm2can(group[1]),group[0]+3,norm2can(group[1]+3),fill=group[2])
                ret = canvas.create_line(group[0],norm2can(group[1]),group[2],norm2can(group[3]),width = 2, fill=group[4])
                rets.append(ret)
            # sleep(0.0000001*(iterator%88)**2)
        return rets
 
def display(main: Tk, render_canvas: Canvas, render_firework1: Firework,render_firework2: Firework,render_firework3: Firework,ret1,ret2,ret3, iterator = 0):
    # render_canvas.delete("all")
    ret1 = render_firework1.render(render_canvas, iterator,ret1)
    ret2 = render_firework2.render(render_canvas, iterator,ret2)
    ret3 = render_firework3.render(render_canvas, iterator,ret3)
    main.after(CYCLE, display, main, render_canvas, render_firework1, render_firework2, render_firework3,ret1,ret2,ret3,iterator + 1)


if __name__ == '__main__':
    window = Tk()  # 一个Tk
    window.title("陪你看烟花")
    canvas = Canvas(window, bg="black", height=CANVAS_HEIGHT, width=CANVAS_WIDTH)
    img = get_img("./src/star_house.jpg", 800, 600)
    canvas.create_image(CANVAS_CENTER_X, CANVAS_CENTER_Y, image=img)
    canvas.pack() 
    firework1 = Firework()  # 调用烟花类
    firework2 = Firework()
    firework3 = Firework()
    display(window, canvas, firework1,firework2,firework3,[],[],[])  # 开始画画~
    window.mainloop()           
