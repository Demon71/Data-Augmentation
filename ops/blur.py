# 作者：MZY
# 开发日期：2023/7/25
# 按指定量模糊图像	blur_1.5

from skimage.filters import gaussian
from skimage.exposure import rescale_intensity
import re
import cv2

CODE = 'blur'
REGEX = re.compile(r"^" + CODE + "_(?P<sigma>[.0-9]+)")

class Blur:
    def __init__(self, sigma):
        self.code = CODE + str(sigma)
        self.sigma = sigma

    def process(self, img):
        return cv2.GaussianBlur(img, (0, 0), self.sigma)

    @staticmethod
    def match_code(code):
        match = REGEX.match(code)
        if match:
            d = match.groupdict()
            return Blur(float(d['sigma']))

