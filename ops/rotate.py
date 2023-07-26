# 作者：MZY
# 开发日期：2023/7/25
# 旋转指定角度，示例：rot_90，rot_-45，正值为逆时针旋转
from skimage import transform
import re
import numpy as np


PREFIX = 'rot'
REGEX = re.compile(r"^" + PREFIX + "_(?P<angle>-?[0-9]+)")

class Rotate:
    def __init__(self, angle):
        self.angle = angle
        self.code = PREFIX + str(angle)

    def process(self, img):
        return (transform.rotate(img, -self.angle)*255).astype(np.uint8)

    @staticmethod
    def match_code(code):
        match = REGEX.match(code)
        if match:
            d = match.groupdict()
            return Rotate(int(d['angle']))
