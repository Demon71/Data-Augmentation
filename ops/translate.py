# 作者：MZY
# 开发日期：2023/7/25
# 输入图片左上角为（0，0）点，向右和向下分别是x轴和y轴正方向,trans_20_10表示向右（x正方向）挪动20，向下（y正方向）挪动10
from skimage.transform import AffineTransform
from skimage import transform as tf
import re
import numpy as np

CODE = 'trans'
REGEX = re.compile(r"^" + CODE + "_(?P<x_trans>[-0-9]+)_(?P<y_trans>[-0-9]+)")

class Translate:
    def __init__(self, x_trans, y_trans):
        self.code = CODE + str(x_trans) + '_' + str(y_trans)
        self.x_trans = x_trans
        self.y_trans = y_trans

    def process(self, img):
        return (tf.warp(img, AffineTransform(translation=(-self.x_trans, -self.y_trans)))*255).astype(np.uint8)

    @staticmethod
    def match_code(code):
        match = REGEX.match(code)
        if match:
            d = match.groupdict()
            return Translate(int(d['x_trans']), int(d['y_trans']))