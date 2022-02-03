import dlib
import cv2


detector = dlib.get_frontal_face_detector() #获取人脸分类器

# opencv 读取图片，并显示
filename = '../3.jpg'
# 将图片加载成一个MAT对象，
img = cv2.imread(filename, cv2.IMREAD_COLOR)
# 注意，这里是生成的三个独立的大矩阵
#print(img)

# 分离三个颜色通道
b, g, r = cv2.split(img)
#print(b)
# 融合三个通道生成新得图片
img2 = cv2.merge([r, g, b])
# 这里生成的是若个小的三维矩阵的和



# 使用detector进行人脸监测，dets为返回的结果
dets = detector(img,1)
# 这里是输出检测的人脸数量
print("Number of faces detected: {}".format(len(dets)))
#
for index, face in enumerate(dets):
    print('face {}; left {}; top {}; right {}; bottom {}'.format(index, face.left(), face.top(), face.right(), face.bottom()))

    # 在图片中标注人脸，并显示
    left = face.left()
    top = face.top()
    right = face.right()
    bottom = face.bottom()
    cv2.rectangle(img, (left, top), (right, bottom), (0, 255, 0), 3)
    # 创建一个opencv窗口，由opencv自动创建和释放，无需销毁他
    cv2.namedWindow(filename, 0)
    # 将图片显示到特定窗口上
    cv2.imshow(filename, img)

# waitKey读取键盘输入，括号里的是等待时间，0表示一直等待
k=cv2.waitKey(0)
# 当选中屏幕，摁ESC推出
if k ==27:     # 键盘上Esc键的键值
  cv2.destroyAllWindows()

