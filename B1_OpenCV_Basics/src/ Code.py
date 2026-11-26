import cv2 as cv
#import numpy as np
#import matplotlib.pyplot as plt

img=cv.imread(r"D:\Gaoyitong often use\Pictures\Camera Roll\dax8um7r4u.jpeg")

#判断读取是否失败
if img is None:
   raise FileNotFoundError("无法读取图像") 

#转灰度      
'''gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

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

#亮度和对比度调整
adjusted = cv.convertScaleAbs(img, alpha=1.8, beta=30)

comparison = cv.hconcat([img, adjusted])
cv.imwrite("brightness_contrast_comparison.jpg", comparison)
cv.imshow("before | after", comparison)'''

# 获取原图高度、宽度
height, width = img.shape[:2]

# 裁剪图像中央区域：保留中间一半的行和列
cropped = img[height//4:3*height//4,
              width//4:3*width//4].copy()

# 保持宽高比例，将裁剪图调整为与原图等高
crop_h, crop_w = cropped.shape[:2]
new_width = round(crop_w * height / crop_h)
cropped_display = cv.resize(cropped, (new_width, height))

# 左边原图，右边裁剪后的放大图
comparison = cv.hconcat([img, cropped_display])

cv.imwrite("cropped.jpg", cropped)
cv.imwrite("crop_comparison.jpg", comparison)

cv.imshow("Original | Cropped (enlarged)", comparison)
cv.waitKey(0)
cv.destroyAllWindows()
