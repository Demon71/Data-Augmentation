# 输入图片左上角为（0，0）点，向右和向下分别是x轴和y轴正方向。输入的四个参数为最后裁剪图片的左上角坐标和右下角坐标
from skimage import transform
import numpy as np
import re

PREFIX = 'zoom'     # 作为生成代码的前缀
# 正则表达式，匹配生成代码的格式
REGEX = re.compile(r"^" + PREFIX + "_(?P<p1x>[-0-9]+)_(?P<p1y>[-0-9]+)_(?P<p2x>[-0-9]+)_(?P<p2y>[-0-9]+)")
PAD_VALUE = 0   # 设置填充值为0

class Zoom:
    def __init__(self, p1x, p1y, p2x, p2y):
        # 定义四个参数，左上角坐标（p1x，p1y），右下角坐标（p2x，p2y）
        self.p1x = p1x
        self.p1y = p1y
        self.p2x = p2x
        self.p2y = p2y
        self.code = PREFIX + str(p1x) + '_' + str(p1y) + '_' + str(p2x) + '_' + str(p2y)    # 存储生成的代码

    def process(self, img):
        # 获取输入图片的宽高
        h = len(img)
        w = len(img[0])

        # 根据给定的参数 p1x、p1y、p2x 和 p2y，计算出裁剪的区域，并将其保存为 cropped_img
        crop_p1x = max(self.p1x, 0)
        crop_p1y = max(self.p1y, 0)
        crop_p2x = min(self.p2x, w)
        crop_p2y = min(self.p2y, h)
        cropped_img = img[crop_p1y:crop_p2y, crop_p1x:crop_p2x]

        # 根据裁剪后的图像尺寸和给定的参数，计算需要进行的填充量
        x_pad_before = -min(0, self.p1x)
        x_pad_after  =  max(0, self.p2x-w)
        y_pad_before = -min(0, self.p1y)
        y_pad_after  =  max(0, self.p2y-h)
        # 使用 np.pad 函数对裁剪后的图像进行填充，使其尺寸与原始图像相同
        padding = [(y_pad_before, y_pad_after), (x_pad_before, x_pad_after)]
        is_colour = len(img.shape) == 3

        if is_colour:
            padding.append((0,0)) # colour images have an extra dimension

        padded_img = np.pad(cropped_img, padding, 'constant')
        # 使用 transform.resize 函数将填充后的图像缩放至原始图像的尺寸，并返回处理后的图像。
        return (transform.resize(padded_img, (h,w))*255).astype(np.uint8)

    # match_code 是一个静态方法，它接受一个代码字符串作为输入，并尝试匹配该字符串是否符合预定义的代码格式。
    # 如果匹配成功，则提取出相应的参数 p1x、p1y、p2x 和 p2y，并用它们创建一个新的 Zoom 对象，并返回该对象。
    @staticmethod
    def match_code(code):
        match = REGEX.match(code)
        if match:
            d = match.groupdict()
            return Zoom(int(d['p1x']), int(d['p1y']), int(d['p2x']), int(d['p2y']))