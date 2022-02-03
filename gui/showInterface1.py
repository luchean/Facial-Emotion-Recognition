import time
import cv2

# 下述包分别对应疲劳度检测、表情预测和专注度计算等不同的维度
from drowsinessDetector import drowsiness
from focusJudge import focus
from model import Predict

# 进行实时绘图，回值疲劳度和表情出现的折线图
import matplotlib.pyplot as plt

def emotionResume(emotionDict):
    '''
    :dicpt:将表情字典进行归零，便于下一次开始运算
    :param emotionDict:
    :return:
    '''
    emotionDict['listening'] = 0
    emotionDict['confused'] = 0
    emotionDict['distracted'] = 0
    emotionDict['tired'] = 0
    emotionDict['confused'] = 0

# 坐标轴的纵坐标
x = list()
# 保存用户的专注度数列
FocusList = list()
# 保存用户的疲劳度list
DrowsinessList = list()
# 将plt变为非交互模式
plt.ion()

# 打开摄像头，并显示对应的结果
print("[INFO] starting video stream thread...")
vs = cv2.VideoCapture(0)
time.sleep(1.0)

# 生成对应疲劳度检测对象
drowsinessDetector = drowsiness.drowsinessDetector()

# 初始化疲劳度的值
drowsinessValue = 0

# 初始化表情的值
learningEmotion = "None"

# 初始化专注度
focusValue = 0

# 初始化表情统计字典
emotionDict ={'listening':0,'distracted':0,'tired':0,'confused':0,'understanding':0,'None':0}

# 计数器，记录帧数
count = 0

# 循环每一帧并进行判定
while True:

    # 读取视频的每一帧，并进行计数
    temp, frame = vs.read()
    count = count + 1

    # 判定帧是否为空
    if frame is None:
        continue

    # 每10帧就进行一次统计
    if count % 10 == 0:
        drowsinessValue += drowsinessDetector.detect(frame)
        learningEmotion = Predict.predictFrame(frame)
        print('the facial emotion is ',learningEmotion)
        print('the drowsiness is ',drowsinessValue)

    # 记录100帧之内的所有的表情
    if count % 150 != 0:
        emotionDict[learningEmotion] = emotionDict[learningEmotion]+1
    else:
        # 标注当前表情的点

        # 计算专注度
        focusValue = focus.focusJudge(emotionDict, drowsinessValue/15)
        # 十个点之内的进行描点划线
        if len(x) < 20 and len(FocusList) < 20 and len(DrowsinessList) < 20:
            DrowsinessList.append(drowsinessValue/15)
            FocusList.append(focusValue)
            if len(x) == 0:
                x.append(0)
            else:
                x.append(x[len(x)-1]+1)
        else:
        # 超过了十个点，就开始一次删除列表中的第一个点
            DrowsinessList.pop(0)
            DrowsinessList.append(drowsinessValue/30)
            FocusList.pop(0)
            FocusList.append(focusValue)
            x.pop(0)
            x.append(x[len(x)-1]+1.5)
            
        # 绘制对应图线
        plt.plot(x,FocusList,color='red')

        plt.plot(x,DrowsinessList,color = 'yellow')

        plt.show(block=False)
        plt.close('all')

        # 到达了150帧，就将所有的表情记录值进行清空
        emotionResume(emotionDict)


    # 实时显示专注度
    focusText = 'Focus Value:'+str(round(focusValue,3))

    # 实时显示当前识别的表情
    emotionText = "learning emotion:" + learningEmotion

    # 实时显示疲劳度
    drowsinessText = "drowsiness Value:"+str(round(drowsinessValue,3))

    # 具体显示如下
    cv2.putText(frame, emotionText, (300, 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    cv2.putText(frame, drowsinessText, (5, 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    cv2.putText(frame, focusText, (5, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    # 将每一帧显示在屏幕上
    cv2.imshow("FocusDetector",frame)
    key = cv2.waitKey(1) & 0xFF

    # 如果按下q键，就退出
    if key == ord("q"):
        break

# 清空所有的窗口
cv2.destroyAllWindows()