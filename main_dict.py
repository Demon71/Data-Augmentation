# 作者：MZY
# 开发日期：2023/7/25
import sys, os, re, traceback
from os.path import isfile
from multiprocessing.dummy import Pool
from counter import Counter
from ops.rotate import Rotate   # 旋转指定角度，示例：rot_90，rot_-45，正值90为逆时针旋转90度
from ops.fliph import FlipH     # 水平翻转	fliph
from ops.flipv import FlipV     # 垂直翻转	flipv
from ops.zoom import Zoom       # 放大(裁剪)图像的指定区域，根据需要执行拉伸/收缩	zoom_0_0_20_20,zoom_-10_-20_10_10
# 输入图片左上角为（0，0）点，向右和向下分别是x轴和y轴正方向。输入的四个参数为最后裁剪图片的左上角坐标和右下角坐标，zoom_0_0_20_20即保留(0，0)(20，20)之间的图像
from ops.blur import Blur       # 按指定量模糊图像	blur_1.5
from ops.noise import Noise     # 向图像添加随机噪声	noise_0.01,noise_0.5
from ops.translate import Translate     # 在x和y方向上按指定量移动图像的像素	trans_20_10表示向右（x正方向）挪动20，向下（y正方向）挪动10,trans_-10_0
from ops.crop_center import Cropcenter  # 中心裁剪正方形的区域。cropcen_300表示将以原图像中心为中心裁剪300*300的大小区域。不能比原图像的像素大
from ops.crop_random import CropRandom  # 随机裁剪正方形的区域。cropran_400_2表示随机在图像中裁剪400*400的区域，并且命名编号为2，可以命名多个不同编号生成多张400*400的随机图像。
from skimage.io import imread, imsave


EXTENSIONS = ['png', 'jpg', 'jpeg', 'bmp']
WORKER_COUNT = max(os.cpu_count() - 1, 1)
OPERATIONS = [Rotate, FlipH, FlipV, Translate, Noise, Zoom, Blur, Cropcenter, CropRandom]

'''
Augmented files will have names matching the regex below, eg

    original__rot90__crop1__flipv.jpg

'''
AUGMENTED_FILE_REGEX = re.compile('^.*(__.+)+\\.[^\\.]+$')
EXTENSION_REGEX = re.compile('|'.join(['.*\\.' + n + '$' for n in EXTENSIONS]), re.IGNORECASE)

thread_pool = None
counter = None

def build_augmented_file_name(original_name, ops):
    root, ext = os.path.splitext(original_name)
    result = root
    for op in ops:
        result += '__' + op.code
    return result + ext

def work(d, f, op_lists):
    try:
        in_path = os.path.join(d,f)
        for op_list in op_lists:
            out_file_name = build_augmented_file_name(f, op_list)
            if isfile(os.path.join(d,out_file_name)):
                continue
            img = imread(in_path)
            for op in op_list:
                img = op.process(img)
            imsave(os.path.join(d, out_file_name), img)

        counter.processed()
    except:
        traceback.print_exc(file=sys.stdout)

def process(dir, file, op_lists):
    thread_pool.apply_async(work, (dir, file, op_lists))



if __name__ == '__main__':
    # 操作：在同一个’‘下写多个操作将对一张图片执行多个操作并保存一张图片，写多个’‘将对一张图片分别执行不同操作并保存多个图片
    # rot_90、水平翻转fliph、垂直翻转flipv、放大/缩小指定区域zoom_0_0_20_20、模糊图像blur_1.5、随机噪声noise_0.01、定量移动图像trans_20_10、中心裁剪cropcen_300、随机裁剪cropran_400_2
    dir_op = ['F:\pythonProject\pretreatment\测试图片', 'zoom_-145_-145_800_800', 'blur_0.5', 'flipv,fliph']

    if len(dir_op) < 2:
        print('Usage: {} <image directory> <operation> (<operation> ...)'.format(dir_op[0]))
        sys.exit(1)

    image_dir = dir_op[0]
    if not os.path.isdir(image_dir):
        print('Invalid image directory: {}'.format(image_dir))
        sys.exit(2)

    op_codes = dir_op[1:]  # 后面的操作步骤
    op_lists = []
    for op_code_list in op_codes:
        op_list = []
        for op_code in op_code_list.split(','):
            op = None
            for op in OPERATIONS:
                op = op.match_code(op_code)
                if op:
                    op_list.append(op)
                    break

            if not op:
                print('Unknown operation {}'.format(op_code))
                sys.exit(3)
        op_lists.append(op_list)

    counter = Counter()
    thread_pool = Pool(WORKER_COUNT)
    print('Thread pool initialised with {} worker{}'.format(WORKER_COUNT, '' if WORKER_COUNT == 1 else 's'))

    matches = []
    for dir_info in os.walk(image_dir):
        dir_name, _, file_names = dir_info
        print('Processing {}...'.format(dir_name))

        for file_name in file_names:
            if EXTENSION_REGEX.match(file_name):
                if AUGMENTED_FILE_REGEX.match(file_name):
                    counter.skipped_augmented()
                else:
                    process(dir_name, file_name, op_lists)
            else:
                counter.skipped_no_match()
    print("Waiting for workers to complete...")
    thread_pool.close()
    thread_pool.join()

    print(counter.get())
