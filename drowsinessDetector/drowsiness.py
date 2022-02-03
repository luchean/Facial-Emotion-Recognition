from scipy.spatial import distance as dist
from imutils import face_utils
from threading import Thread
import winsound
import imutils
import time
import dlib
import cv2

def sound_alarm(path):
	# play an alarm sound
	winsound.PlaySound(path,winsound.SND_FILENAME)

'''
    描述：计算EAR值，判定眼睛的具体情况
    参数：传入的是眼部特征所对应的点
    返回：最终的EAR的计算结果
'''
def eye_aspect_ratio(eye):

    # compute the vertical distance of the eye
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])

    # compute the horizal distance of two eyes
    C = dist.euclidean(eye[0], eye[3])

    # compute the eye aspect ratio  of two eyes
    ear = (A + B) / (2.0 * C)

    # return the eye aspect ratio
    return ear

class drowsinessDetector:

    # 实时记录闭眼睛的次数和警报器是否已经开启
    COUNTER = 0
    ALARM_ON = False

    # define the constants to judge status
    # judge whether the eye is closed
    EYE_AR_THRESH = 0.25

    # the number of the frames where the EAR is below the threshold
    EYE_AR_CONSEC_FRAMES = 24

    # define the path of the video you will process
    # the path of the face detector
    pathPedictor = r"C:\Users\gray\Desktop\FacialEmotionRecognition\shape_predictor_68_face_landmarks.dat"

    # the path of alarm video
    pathAlarm = "C:\\Users\\gray\\Desktop\\FacialEmotionRecognition\\alarm.wav"

    def __init__(self):

        # initialize dlib's face detector (HOG-based) and then create
        # the facial landmark predictor
        print("[INFO] loading facial landmark predictor...")
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor(drowsinessDetector.pathPedictor)

        # grab the indexes of the facial landmarks for the left and
        # right eye, respectively
        self.lStart = 0
        self.lEnd = 0
        self.rStart = 0
        self.rEnd = 0
        (self.lStart, self.lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
        (self.rStart, self.rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]



    def detect(self,frame):

        # 对帧进行重置大小
        frame = imutils.resize(frame, width=450)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # detect faces in the grayscale frame
        rects = self.detector(gray, 0)

        # loop over the face detections
        for rect in rects:
            # determine the face region and convert it into coordinates
            shape = self.predictor(gray, rect)
            shape = face_utils.shape_to_np(shape)

            # extract the left and right eye coordinates, then use the
            # coordinates to compute the eye aspect ratio for both eyes
            leftEye = shape[self.lStart:self.lEnd]
            rightEye = shape[self.rStart:self.rEnd]
            leftEAR = eye_aspect_ratio(leftEye)
            rightEAR = eye_aspect_ratio(rightEye)

            # average the eye aspect ratio together for both eyes
            ear = (leftEAR + rightEAR) / 2.0

            # compute the convex hull for the left and right eye, then
            # # visualize each of the eyes
            # leftEyeHull = cv2.convexHull(leftEye)
            # rightEyeHull = cv2.convexHull(rightEye)
            #
            # #  标记出每一只眼睛
            # cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
            # cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)

            # check if the EAR is below the threshold
            if ear < drowsinessDetector.EYE_AR_THRESH:
                drowsinessDetector.COUNTER += 1

                # if the eyes are closed for a long enough time then you will sound alarm
                if drowsinessDetector.COUNTER >= drowsinessDetector.EYE_AR_CONSEC_FRAMES:

                    # if the alarm is not on, turn it on
                    if not drowsinessDetector.ALARM_ON:
                        drowsinessDetector.ALARM_ON = True

                        # check to see if an alarm file was supplied,
                        # and if so, start a thread to have the alarm
                        # sound played in the background
                        if drowsinessDetector.pathAlarm != "":
                            t = Thread(target=sound_alarm,
                                       args=(drowsinessDetector.pathAlarm,))
                            t.deamon = True
                            t.start()


            # otherwise the sys aspect ratio is not blow the blink
            # reset the conuter and set the alarmfalse
            else:
                drowsinessDetector.COUNTER = 0
                drowsinessDetector.ALARM_ON = False


        return drowsinessDetector.COUNTER/15