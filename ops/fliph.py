# 作者：MZY
# 开发日期：2023/7/25
# 水平翻转	fliph

import numpy as np

CODE = 'fliph'

class FlipH:
    def __init__(self):
        self.code = CODE

    def process(self, img):
        return np.fliplr(img)

    @staticmethod
    def match_code(code):
        if code == CODE:
            return FlipH()