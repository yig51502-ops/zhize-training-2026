import cv2 as cv
#import numpy as np
#import matplotlib.pyplot as plt

img=cv.imread(r"D:\Gaoyitong often use\Pictures\Camera Roll\dax8um7r4u.jpeg")

#判断读取是否失败
if img is None:
   raise FileNotFoundError("无法读取图像") 

#转灰度      
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

#加载 Haar 人脸分类器
from pathlib import Path
import shutil

xml_name = "haarcascade_frontalface_default.xml"
source_xml = Path(cv.__file__).resolve().parent / "data" / xml_name
local_xml = Path(__file__).resolve().parent / xml_name

if not local_xml.exists():
    shutil.copyfile(source_xml, local_xml)

face_cascade = cv.CascadeClassifier(str(local_xml))

if face_cascade.empty():
    raise RuntimeError("Haar 人脸分类器加载失败")

#检测人脸
faces = face_cascade.detectMultiScale(gray, 1.1, 5)

#在 for 循环内完成局部高斯模糊并写回
for x, y, w, h in faces:
    face = img[y:y+h, x:x+w]
    blurred = cv.GaussianBlur(face, (15, 15), 0)
    img[y:y+h, x:x+w] = blurred

cv.imwrite("output.jpg", img)
cv.imshow("result", img)
cv.waitKey(0)
cv.destroyAllWindows()
