[B.1 OpenCV 基础图像处理与人脸模糊.md](https://github.com/user-attachments/files/35467172/B.1.OpenCV.md)
# B\.1 OpenCV 基础图像处理与人脸模糊

# 一\.代码及解释

## 1\.重点部分

### **图像读取、显示与保存**

```Plain Text
import cv2

img = cv2.imread("images/test.jpg", cv2.IMREAD_COLOR)

if img is None:
    raise FileNotFoundError("图像读取失败，请检查路径")

cv2.imshow("image", img)
cv2.waitKey(0)
cv2.destroyAllWindows()

cv2.imwrite("output/result.jpg", img)
```

- `cv2.imread(path, flag)`：读取图像。

    - `cv2.IMREAD_COLOR`：彩色图，默认 BGR。

    - `cv2.IMREAD_GRAYSCALE`：灰度图。

    - `cv2.IMREAD_UNCHANGED`：保留透明通道等原始信息。

- `cv2.imshow(window_name, img)`：显示图像。

- `cv2.waitKey(0)`：等待键盘输入，否则窗口可能立即关闭。

- `cv2.destroyAllWindows()`：关闭窗口。

- `cv2.imwrite(path, img)`：保存图像，格式通常由扩展名决定。

文件路径常见问题：

```Plain Text
from pathlib import Path

path = Path(r"D:\images\test.jpg")
img = cv2.imread(str(path))
```

注意：

- Windows 路径建议使用原始字符串 `r"..."`、正斜杠 `/` 或 `Path`。

- 相对路径相对于当前工作目录，不一定是脚本所在目录，可以用：

```Plain Text
import os
print(os.getcwd())
```

- 读取失败时，\`imread\` 通常返回 `None`，应当检查。

- Windows 中文路径在部分 OpenCV 环境中可能读取失败，可以使用：

```Plain Text
import cv2
import numpy as np

data = np.fromfile("测试图片.jpg", dtype=np.uint8)
img = cv2.imdecode(data, cv2.IMREAD_COLOR)

ok, buffer = cv2.imencode(".jpg", img)
if ok:
    buffer.tofile("保存结果.jpg")
```

---

### **像素访问、图像属性、区域和裁剪**

```Plain Text
print(img.shape)
print(img.dtype)
print(img[100, 200])
```

彩色图像通常具有：

```Plain Text
img.shape == (高度, 宽度, 通道数)
```

例如：

```Plain Text
(480, 640, 3)
```

表示高度 480、宽度 640、3 个通道。

OpenCV 的彩色顺序是 **BGR**：

```Plain Text
b, g, r = img[100, 200]
```

访问和修改像素：

```Plain Text
pixel = img[y, x]
img[y, x] = [255, 0, 0]  # BGR 中的蓝色
```

坐标顺序是：

```Plain Text
img[y, x]
```

不是 `img[x, y]`。

图像裁剪使用 NumPy 切片：

```Plain Text
roi = img[y1:y2, x1:x2]
```

规律：

- `y` 对应行，也就是高度方向。

- `x` 对应列，也就是宽度方向。

- 起始位置包含，结束位置不包含。

- `img[y1:y2, x1:x2]` 通常是原图的视图。

如果需要独立副本：

```Plain Text
roi = img[y1:y2, x1:x2].copy()
```

直接修改 ROI 会影响原图：

```Plain Text
img[50:150, 100:200] = [0, 255, 0]
```

---

### **算术运算、亮度和对比度**

图像像素通常是 `uint8`，范围为 `0~255`。

直接进行 NumPy 运算可能发生溢出：

```Plain Text
bright = img + 100
```

`uint8` 超过 255 后可能回绕，而不是自动限制在 255。

推荐使用 OpenCV 的饱和运算：

```Plain Text
bright = cv2.add(img, 50)
```

亮度和对比度可以写成：

```Plain Text
result = cv2.convertScaleAbs(img, alpha=1.2, beta=20)
```

其中：

```Plain Text
new_pixel = old_pixel * alpha + beta
```

- `alpha > 1`：提高对比度。

- `alpha < 1`：降低对比度。

- `beta > 0`：提高亮度。

- `beta < 0`：降低亮度。

也可以使用：

```Plain Text
result = cv2.addWeighted(img, 1.2, img, 0, 20)
```

需要理解的核心问题：

- 像素值不能低于 0 或高于 255。

- OpenCV 的部分函数会自动截断到合法范围。

- NumPy 的 `uint8` 运算可能产生溢出。

- 乘法运算通常需要转成浮点数，再裁剪并转换回 `uint8`。

---

### **平滑滤波，尤其是高斯滤波**

```Plain Text
blur = cv2.GaussianBlur(img, (5, 5), 0)
```

参数含义：

- `(5, 5)`：高斯核大小。

- 核大小通常使用正奇数，例如 `(3,3)`、\`\(5,5\)\`、\`\(7,7\)\`。

- 最后的 `0` 表示让 OpenCV 自动计算标准差。

理解重点：

- 高斯滤波可以减少噪声。

- 核越大，平滑效果越强。

- 平滑越强，细节和边缘也越容易被削弱。

- 在边缘检测、阈值分割前，常先进行高斯滤波。

- 核大小不能随意设置得过大，否则图像会变得模糊。

---

## **2\.略看部分**

### **2\.1 BGR、RGB、灰度和 HSV**

OpenCV 默认使用 BGR：

```Plain Text
bgr = cv2.imread("test.jpg")
rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
```

用途：

- BGR：OpenCV 默认格式。

- RGB：Matplotlib、PIL 等工具常用。

- 灰度图：减少计算量，常用于人脸检测、边缘检测和阈值处理。

- HSV：颜色分割时更方便，例如提取特定颜色区域。

---

### **2\.2 绘图、窗口和视频读取**

静态图片阶段先了解常用函数：

```Plain Text
cv2.line(...)
cv2.rectangle(...)
cv2.circle(...)
cv2.putText(...)
```

视频读取的基本形式：

```Plain Text
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    cv2.imshow("camera", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
```

暂时重点理解：

- `VideoCapture` 打开摄像头或视频文件。

- `read()` 逐帧读取。

- `ret` 表示是否读取成功。

- `release()` 释放资源。

---

### **2\.3 阈值、轮廓、边缘和形态学**

- 阈值分割：把图像分成前景和背景。

- 轮廓：描述物体边界。

- Canny：常用边缘检测方法。

- 腐蚀：缩小白色区域、去除小噪声。

- 膨胀：扩大白色区域、连接断裂部分。

- 开运算：先腐蚀后膨胀，常用于去噪。

- 闭运算：先膨胀后腐蚀，常用于填补空洞。

---

## **3\.NumPy 基础概括**

常见形状：

```Plain Text
彩色图：   (height, width, 3)
灰度图：   (height, width)
带透明度： (height, width, 4)
```

---

## **4\.Haar 级联分类器**

调用流程可以固定记忆为：

1. 加载分类器。

2. 读取图像。

3. 转成灰度图。

4. 调用 `detectMultiScale`。

5. 在检测区域画框。

```Plain Text
import cv2

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades +
    "haarcascade_frontalface_default.xml"
)

img = cv2.imread("test.jpg")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

faces = face_cascade.detectMultiScale(
    gray,
    scaleFactor=1.1,
    minNeighbors=5,
    minSize=(30, 30)
)

for x, y, w, h in faces:
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

cv2.imshow("face", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

- `scaleFactor`：图像缩放比例。

- `minNeighbors`：确认目标所需的邻近检测数量，越大通常越严格。

- `minSize`：允许检测的最小目标尺寸。

- `x, y, w, h`：矩形左上角坐标、宽度和高度。

- 



# 二、总结与收获

### 1\.对“图像是什么”有了具体认识

OpenCV 读进来的彩色图在 Python 里是 numpy\.ndarray，dtype=uint8，shape=\(h, w, 3\)，像素值 0\~255，通道按 BGR 交错存放在一整块连续内存里。所有“图像操作”本质都是对这块数组做索引或数值运算，没有魔法。

### 2\.坐标与下标要分开想

检测框给的是 \(x, y, w, h\)，数组下标是 \[行, 列\]，所以换算成 img\[y:y\+h, x:x\+w\] 是“先行后列”。

### 3\.切片、副本、写回是三种不同的事

- img\[y:y\+h, x:x\+w\] 得到的是视图，和原图共享内存，裁剪这个动作本身不复制、不改像素；

- \.copy\(\) 才是独立副本，后续改动不影响原图；

- img\[y:y\+h, x:x\+w\] = blurred 是原地写入，这一步才真正改动了原图对应区域。

模糊之所以“看起来生效”，不是因为切片，而是因为最后这次赋值。

### 4\.高斯核变大，改变的是视觉效果，而不是检测结果

\(5,5\) 换成 \(31,31\)，参与平滑的邻域变大，模糊更强、细节更少（核必须是奇数）。但流程是“先检测、再模糊”，所以换核大小不会改变已经得到的 faces。 “减少误检、增加漏检”属于 minNeighbors、scaleFactor 这类检测参数的范畴——这两类参数作用的阶段不同，我一开始把它们混在一起，是这次最值得记住的一次纠正。

### 5\.参数要先问“它作用在哪一步”

亮度/对比度、模糊核、检测阈值，分别作用在像素值、邻域、候选框三个层面。拿到一个新参数，先定位它在流水线的哪一段，再谈它“会带来什么影响”，比背结论可靠得多。

