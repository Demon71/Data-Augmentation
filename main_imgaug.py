# 作者：MZY
# 开发日期：2023/7/25
# 使用imgaug库，实现图像变换，在主函数中定义所需要的不同的增强操作，并放在列表中准备依次调用
import os
import imageio
from imgaug import augmenters as iaa
from skimage.io import imread, imsave
import imgaug as ia


class MyAugMethod():

    def __init__(self):
        self.imglist_name = []
        self.imglist = []

    # 遍历输入文件夹，返回所有图片名称
    def show_path_file(self, inputpath, all_files_name, all_files):
        # 首先遍历当前目录所有文件及文件夹
        file_list = os.listdir(inputpath)
        # 保存图片文件的目录
        last_path = inputpath
        # 准备循环判断每个元素是否是文件夹还是文件，
        # 是文件的话，把名称传入list，是文件夹的话，递归
        for filename in file_list:
            # 利用os.path.join()方法取得路径全名，并存入cur_path变量
            # 否则每次只能遍历一层目录
            cur_path = os.path.join(inputpath, filename)
            # 判断是否是文件夹
            if os.path.isdir(cur_path):
                last_path = cur_path
                self.show_path_file(cur_path, all_files_name, all_files)
            else:
                filename = os.path.join(last_path, filename)
                all_files_name.append(filename)
                all_files.append(imageio.v2.imread(filename))

    # 定义增强的方法
    def aug_method(self, image, augmentations):
        # 定义组合的增强方法
        seq = iaa.Sequential(augmentations)
        # 对输入图片应用组合的增强方法
        augmented_image = seq.augment_image(image)
        return augmented_image

    # 数据增强函数
    def aug_data(self, inputpath, augmentations_list):
        # 获得输入文件夹中的文件列表
        self.show_path_file(inputpath, self.imglist_name, self.imglist)

        # 对每张图片应用增强方法
        for index in range(len(self.imglist)):
            original_image = self.imglist[index]

            # 对每个图片分别应用不同的增强操作
            for i, augmentations in enumerate(augmentations_list):
                augmented_image = self.aug_method(original_image, augmentations)
                print("aug data for {} times ".format(i))
                # 保存图片
                filename = self.imglist_name[index].split(".png", 1)[0]
                imsave(filename + "_{}.png".format(i + 1), augmented_image)


if __name__ == "__main__":
    # 图片文件相关路径
    inputpath = 'F:\pythonProject\pretreatment\测试图片'
    ia.seed(1)
    # 定义基本增强操作
    aug1 = iaa.Affine(rotate=(40, 70))  # 旋转
    aug2 = iaa.Affine(scale=(0.5, 0.9))  # 将图像缩放到原始大小的50到90％的值
    aug3 = iaa.Sequential([  # 按预定义顺序应用,缩放+任选一种进行模糊
        iaa.Affine(scale=(0.5, 1.5)),
        iaa.OneOf([  # 应用其中的一个模糊操作
            iaa.Superpixels(p_replace=0.3, n_segments=64),  # 生成大约64个超像素。 用平均像素颜色替换每个概率为50％
            iaa.GaussianBlur(sigma=(0.6, 1.5)),  # 用高斯内核模糊每个图像
            iaa.Multiply((0.5, 1.5)),   # 图像中的所有像素与特定值相乘，从而使图像更暗或更亮
            iaa.AddElementwise((-40, 40)),  # 在图像中添加-40到40之间的随机值，每个像素采样一次
            iaa.CoarseDropout(0.02, size_percent=0.5),  # 将所有像素转换为黑色像素来丢弃2％
            iaa.Dropout(p=(0.05, 0.15)),    # 将图像中％像素转换为黑色像素
        ])
    ])

    # 将需要的增强操作放入一个列表中
    # 对一个图片多次操作，在列表中写入多个增强操作
    # 将一张图片旋转为多个角度的图
    augmentations_list = [aug1, aug2, aug3]
    test = MyAugMethod()
    test.aug_data(inputpath, augmentations_list)  # 执行操作

