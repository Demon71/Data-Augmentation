# 作者：MZY
# 开发日期：2023/7/25
# 中心裁剪正方形的区域
from skimage import transform
import re
import numpy as np

PREFIX = 'cropcen'
REGEX = re.compile(r"^" + PREFIX + "_(?P<size>[0-9]+)")

class Cropcenter:
    def __init__(self, size):
        self.size = size
        self.code = PREFIX + str(size)

    def process(self, img):
        h, w = img.shape[:2]
        center_y, center_x = h // 2, w // 2
        half_size = self.size // 2
        cropped_img = img[center_y - half_size: center_y + half_size, center_x - half_size: center_x + half_size]
        resized_img = transform.resize(cropped_img, (h, w), mode='constant')
        return (resized_img * 255).astype(np.uint8)

    @staticmethod
    def match_code(code):
        match = REGEX.match(code)
        if match:
            d = match.groupdict()
            return Cropcenter(int(d['size']))
