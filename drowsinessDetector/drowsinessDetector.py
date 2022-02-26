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


# define the path of the video you will process
# the path of the face detector
pathPedictor = r"C:\Users\gray\Desktop\FacialEmotion\Facial-Emotion-Recognition\Tools\DataTool\shape_predictor_68_face_landmarks.dat"

# the path of alarm video
pathAlarm = "C:\\Users\\gray\\Desktop\\FacialEmotionRecognition\\alarm.wav"

# define the constants to judge status
# judge whether the eye is closed
EYE_AR_THRESH = 0.25
# the number of the frames where the EAR is below the threshold
EYE_AR_CONSEC_FRAMES = 48

# intialize the frame counters and the total number of the blinks

# the total number of successive frames when your eyes are closed
COUNTER = 0
# a boolean to indicates whether the alarm is going off
ALARM_ON = False

# initialize dlib's face detector (HOG-based) and then create
# the facial landmark predictor
print("[INFO] loading facial landmark predictor...")
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(pathPedictor)

# grab the indexes of the facial landmarks for the left and
# right eye, respectively
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

# start the video stream thread
print("[INFO] starting video stream thread...")
vs = cv2.VideoCapture(0)


# loop over frames from the video stream
while True:

    # grab the frame from the threaded video file stream, resize
    # it, and convert it to grayscale
    # channels)
    # read the frame of the video
    temp,frame = vs.read()

    if frame is  None:
    # the resize the size of the frame
        continue
    frame = imutils.resize(frame, width=450)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # detect faces in the grayscale frame
    rects = detector(gray, 0)

    # loop over the face detections
    for rect in rects:
        # determine the face region and convert it into coordinates
        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)

        # extract the left and right eye coordinates, then use the
        # coordinates to compute the eye aspect ratio for both eyes
        leftEye = shape[lStart:lEnd]
        rightEye = shape[rStart:rEnd]
        leftEAR = eye_aspect_ratio(leftEye)
        rightEAR = eye_aspect_ratio(rightEye)

        # average the eye aspect ratio together for both eyes
        ear = (leftEAR + rightEAR) / 2.0

        # compute the convex hull for the left and right eye, then
        # visualize each of the eyes
        leftEyeHull = cv2.convexHull(leftEye)
        rightEyeHull = cv2.convexHull(rightEye)
        #  标记出每一只眼睛
        cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
        cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)

        # check if the EAR is below the threshold
        if ear < EYE_AR_THRESH:
            COUNTER += 1

            # if the eyes are closed for a long enough time then you will sound alarm
            if COUNTER >= EYE_AR_CONSEC_FRAMES:

                # if the alarm is not on, turn it on
                if not ALARM_ON:
                    ALARM_ON = True

                    # check to see if an alarm file was supplied,
                    # and if so, start a thread to have the alarm
                    # sound played in the background
                    if pathAlarm != "":
                        t = Thread(target=sound_alarm,
                                   args=(pathAlarm,))
                        t.deamon = True
                        t.start()

                # display the output on teh frame
                cv2.putText(frame, "DROWSINESS ALERT!", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        # otherwise the sys aspect ratio is not blow the blink
        # reset the conuter and set the alarmfalse
        else:
            COUNTER = 0
            ALARM_ON = False

        # draw the computed  sys aspect ratio on the frame
        cv2.putText(frame,"EAR:{:.2f}".format(ear),(300,30),
                    cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)

    # show the frame, change the ASCII to char
    cv2.imshow("Frame",frame)
    key = cv2.waitKey(1) & 0xFF

    # if the q key was pressed ,break from the loop
    if key == ord("q"):
        break

# clean up the window
cv2.destroyAllWindows()
vs.stop()