# 作者：MZY
# 开发日期：2023/7/25
# 随机裁剪正方形的区域。cropran_400_2表示随机在图像中裁剪400*400的区域，并且命名编号为2，可以命名多个不同编号生成多张400*400的随机图像。

from skimage import transform
import re
import numpy as np
import random

PREFIX = 'cropran'
REGEX = re.compile(r"^" + PREFIX + "_(?P<size>[0-9]+)_(?P<num>[0-9]+)")

class CropRandom:
    def __init__(self, size, num):
        self.size = size
        self.num = num
        self.code = PREFIX + str(size) + '_' + str(num)

    def process(self, img):
        h, w = img.shape[:2]
        max_crop_y = h - self.size
        max_crop_x = w - self.size

        if max_crop_y <= 0 or max_crop_x <= 0:
            raise ValueError("Image size should be larger than the crop size")

        start_y = random.randint(0, max_crop_y)
        start_x = random.randint(0, max_crop_x)

        cropped_img = img[start_y:start_y + self.size, start_x:start_x + self.size]
        resized_img = transform.resize(cropped_img, (h, w), mode='constant')
        return (resized_img * 255).astype(np.uint8)

    @staticmethod
    def match_code(code):
        match = REGEX.match(code)
        if match:
            d = match.groupdict()
            return CropRandom(int(d['size']), int(d['num']))

# from skimage import transform
# import re
# import numpy as np
# import random
#
# PREFIX = 'cropran'
# REGEX = re.compile(r"^" + PREFIX + "_(?P<size>[0-9]+)_(?P<num_images>[0-9]+)")
#
# class CropRandom:
#     def __init__(self, size):
#         self.size = size
#         self.code = PREFIX + str(size)
#
#     def process(self, img):
#         h, w = img.shape[:2]
#         max_crop_y = h - self.size
#         max_crop_x = w - self.size
#
#         if max_crop_y <= 0 or max_crop_x <= 0:
#             raise ValueError("Image size should be larger than the crop size")
#
#         start_y = random.randint(0, max_crop_y)
#         start_x = random.randint(0, max_crop_x)
#
#         cropped_img = img[start_y:start_y + self.size, start_x:start_x + self.size]
#         resized_img = transform.resize(cropped_img, (h, w), mode='constant')
#         return (resized_img * 255).astype(np.uint8)
#
#     @staticmethod
#     def match_code(code):
#         match = REGEX.match(code)
#         if match:
#             d = match.groupdict()
#             return CropRandom(int(d['size']))
#
#     @staticmethod
#     def process_code(code, img):
#         match = REGEX.match(code)
#         if match:
#             d = match.groupdict()
#             size = int(d['size'])
#             num_images = int(d['num_images'])
#             crop_resize = CropRandom(size=size)
#             images = crop_resize.process(img, num_images=num_images)
#             return images
#         else:
#             raise ValueError("Invalid code format")
