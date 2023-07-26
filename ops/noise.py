# 作者：MZY
# 开发日期：2023/7/25
from skimage.util import random_noise
import re
import numpy as np

CODE = 'noise'
REGEX = re.compile(r"^" + CODE + "_(?P<var>[.0-9]+)")

class Noise:
    def __init__(self, var):
        self.code = CODE + str(var)
        self.var = var

    def process(self, img):
        return (random_noise(img, mode='gaussian', var=self.var)*255).astype(np.uint8)

    @staticmethod
    def match_code(code):
        match = REGEX.match(code)
        if match:
            d = match.groupdict()
            return Noise(float(d['var']))
