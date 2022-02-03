from tkinter import *
import tkinter.simpledialog
import time
import cv2
import os

# from Facedata_load import Facedata_load,Facedata_insert
# from Face_Detect import Face_Detect,closecamera,Enter_Face,Face_Detect_img
from Face_Live import Face_Live
from tkinter import filedialog
from PIL import ImageTk
from PIL import Image

BOARD_WIDTH = 1280
BOARD_HEIGHT = 720


main = Tk()

# 前端右上角内容
main.title("Focus_detector_System")
main.geometry('1280x720')
# 禁止改变窗口大小
main.resizable(width=False, height=False)
# 修改图标
main.iconbitmap('image/face_logo.ico')

# 以main为对象，创建了一个tk对象
c1 = Canvas(main, background='#DAE3F3',
    width=BOARD_WIDTH, height=BOARD_HEIGHT)
# 将对应的c1部件妨到窗口中



#图片链接，将图片连接到对应前端页面
bg_img = PhotoImage(file='image/bg_img.png')
# 图片录入按钮
bnt_1 = PhotoImage(file='image/bnt_1.png')
# 摄像头录入按钮
bnt_2 = PhotoImage(file='image/bnt_2.png')
# 打开摄像头
bnt_3 = PhotoImage(file='image/bnt_3.png')
# 活体检测
bnt_4 = PhotoImage(file='image/bnt_4.png')
# 重置
bnt_5 = PhotoImage(file='image/bnt_5.png')
# 暂停
bnt_6 = PhotoImage(file='image/bnt_6.2.png')
# 登录按钮
bnt_7 = PhotoImage(file='image/bnt_7.png')
# 打开摄像头人脸登录
open_img = PhotoImage(file='image/open.png')
# 摄像头关闭1
close_img = PhotoImage(file='image/close.png')

#背景，将对应的图片作为背景进行展示
c1.create_image(BOARD_WIDTH /2, BOARD_HEIGHT/2, image=bg_img)
c1.pack()

# 定义结果展示的字符串
str_jieguo = StringVar()
str_jieguo2 = StringVar()
str_id = StringVar()
str__name = StringVar()
str_sex = StringVar()
# enter_str_id = StringVar()
# enter_str__name = StringVar()
# enter_str_sex = StringVar()
# str_id.set('unknown')
# str__name.set('unknown')
# str_sex.set('unknown')
# id_list = []
# name_list = []
# sex_list = []
# encoding_list = []
#
imgDict = {}


def getImgWidget(filePath):
    '''
        描述：读取filepath对应的图片，转为tkinter可以显示的图片
    '''
    if os.path.exists(filePath) and os.path.isfile(filePath):

        # 文件不为空，并且在已经保存在imgDict中就直接返回图片
        if filePath in imgDict and imgDict[filePath]:
            return imgDict[filePath]

        # 包含从PIL图像创建和修改tkinter位图图像和照片图像的支持，就是显示图片
        img = Image.open(filePath)
        img = ImageTk.PhotoImage(img)
        imgDict[filePath] = img
        return img
    return None

def Emotion_detect():
    '''
    :description:打开实时表情检测的显示
    :parameter:修改标志位变量，主程序根据标志位进行判定是否要打开表情分类
    :return:无返回值
    '''


def PauseFocus():
    '''
    :dict:暂时保存
    :return:
    '''
    c2.place_forget()
    c3.place_forget()
    id.place_forget()
    name.place_forget()
    sex.place_forget()
    result2.place_forget()
    str_jieguo.set('摄像头已暂停')


def Enter_message():
    c2.place(relx=0.309, rely=0.411, anchor=CENTER)
    id = tkinter.simpledialog.askinteger(title = '获取信息',prompt='请输入学号：')
    name = tkinter.simpledialog.askstring(title='获取信息', prompt='请输入姓名：')
    sex = tkinter.simpledialog.askstring(title='获取信息', prompt='请输入性别(0/女，1/男)：')
    flag = 0
    if id!=None and name!=None and sex!=None:
        img_path = filedialog.askopenfilename()
        # flag = Facedata_insert(sql_path,id,name,sex,img_path)
    else:
        pass
    if flag == 1:
        str_jieguo.set(name+'人脸添加成功'+'重置生效')
    else:
        str_jieguo.set("未录入人脸")



def Enter_message_camera():
    id = tkinter.simpledialog.askinteger(title = '获取信息',prompt='请输入学号：')
    name = tkinter.simpledialog.askstring(title='获取信息', prompt='请输入姓名：')
    sex = tkinter.simpledialog.askstring(title='获取信息', prompt='请输入性别(0/女，1/男)：')
    flag = 0
    # str_jieguo.set('按下s保存,按下q退出')
    if id!=None and name!=None and sex!=None:
        print(1111)
        # img_path = Enter_Face(id)
        # flag = Facedata_insert(sql_path,id,name,sex,img_path)
    else:
        pass
    if flag == 1:
        str_jieguo.set(name+'人脸添加成功'+'重置生效')
    else:
        str_jieguo.set("未录入人脸")

def Refresh():
    '''
    :dict:将实时绘制的专注度曲线进行过归零，默认是五分钟进行一次归零，并将数据进行保存
    :return:
    '''

def Drowsiness_detect():
    '''
    :dict:打开疲劳度检测，实时显示对用户疲劳度的检测
        通过改变参数，决定是否要实时显示疲劳度
    :return: 无返回值
    '''


#图片录入按钮
Button(main, text='图片录入', relief=FLAT, cursor = "hand2",bg='#DAE3F3',command =  Enter_message,
       image=bnt_1).place(relx=0.136, rely=0.895, anchor=CENTER)
#摄像头录入按钮
Button(main, text='摄像头录入', relief=FLAT, cursor = "hand2",bg='#DAE3F3',command = Enter_message_camera,
       image=bnt_2).place(relx=0.292, rely=0.895, anchor=CENTER)
#摄像头检测按钮
Button(main, text='表情分析', relief=FLAT, cursor = "hand2",bg='#DAE3F3', command = Emotion_detect(),
       image=bnt_3).place(relx=0.5, rely=0.895, anchor=CENTER)
#活体检测按钮
Button(main, text='疲劳检测', relief=FLAT, cursor = "hand2",bg='#DAE3F3', command =Drowsiness_detect,
       image=bnt_4).place(relx=0.656, rely=0.895, anchor=CENTER)
#重新开始
Button(main, text='数据库重置', relief=FLAT, cursor = "hand2",bg='#DAE3F3',command = Refresh,
       image=bnt_5).place(relx=0.826, rely=0.895, anchor=CENTER)
#关闭摄像头按钮
Button(main, text='关闭摄像头', relief=FLAT, cursor = "hand2",bg='#DAE3F3', command = Close_camera,
       image=bnt_6).place(relx=0.916, rely=0.895, anchor=CENTER)

#相机画布
c2 = Canvas(main, background='#F2F2F2',
    width=640, height=480)

c3 = Canvas(main, background='#F2F2F2',
    width=139, height=170)

c2.create_image(0, 0, anchor='nw', image=open_img )
c2.pack()
c3.pack()


#结果文字显示
id = Label(main, textvariable = str_id, font = ('汉仪晓波折纸体简',15), foreground = 'black',bg='white')
name = Label(main, textvariable = str__name, font = ('汉仪晓波折纸体简',15), foreground = 'black',bg='white')
sex = Label(main, textvariable = str_sex, font = ('汉仪晓波折纸体简',15), foreground = 'black',bg='white')
result = Label(main, textvariable = str_jieguo, font = ('汉仪晓波折纸体简',18), foreground = 'red',bg='#F2F2F2')
result2 = Label(main, textvariable = str_jieguo2, font = ('汉仪晓波折纸体简',16), foreground = 'red',bg='#F2F2F2')
# str_jieguo2.set('name:xxx'+'\n'+'测试结果成功')
result.place(relx=0.82, rely=0.7, anchor= CENTER)
result2.place(relx=0.856, rely=0.18, anchor= CENTER)



if __name__ == "__main__":
    csv_path = 'facedata.csv'
    sql_path = 'Facedata_0.db'
    img_path = r'./getpics/temp.jpg'

    # id_list, name_list, sex_list, encoding_list, text = Facedata_load(csv_path, sql_path)
    # str_jieguo.set(text)

    main.mainloop()
    # closecamera()