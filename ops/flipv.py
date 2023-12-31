# 作者：MZY
# 开发日期：2023/7/25
# 垂直翻转	flipv

import numpy as np

CODE = 'flipv'

class FlipV:
    def __init__(self):
        self.code = CODE

    def process(self, img):
        return np.flipud(img)

    @staticmethod
    def match_code(code):
        if code == CODE:
            return FlipV()