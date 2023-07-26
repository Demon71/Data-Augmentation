# 数据增强器
一共三个主程序，均可以进行增强操作。
main_augment.py文件、main_dict.py文件、main_imgaug.py文件<br/>
main_imgaug.py文件功能最全。可以实现main_augment.py文件、main_dict.py文件的操作
##   
## Image Augmentor
main_augment.py文件
用于在命令行中控制，例如：

    python main.py <image dir> <transform1> <transform2> ...

参数应该是包含要扩充的图像文件的目录的路径
`jpg, jpeg, bmp, png`.

The `transform` arguments 列表代码

|Code| Description |Example Values|
|---|-------------|------|
|`fliph`| 水平翻转        |`fliph`|
|`flipv`| 垂直翻转        |`flipv`|
|`noise`| 随机噪声        |`noise_0.01`,`noise_0.5`|
|`rot`| 旋转角度(正为逆时针) |`rot_90`,`rot_-45`|
|`trans`| 定量移动图像      |`trans_20_10`,`trans_-10_0`|
|`zoom`| 放大/缩小指定区域   |`zoom_0_0_20_20`,`zoom_-10_-20_10_10`|
|`blur`| 模糊图像        |`blur_1.5`|

每个转换参数都会为每个输入图像生成一个额外的输出图像。 参数可以由一个或多个扩充操作组成。单个参数中的多个操作 必须用逗号分隔，并且执行操作的顺序将与操作的顺序匹配 在参数中指定。


### 基本用法
为每个输入图像生成2个输出图像，其中一个水平翻转，另一个垂直翻转：

    python main.py ./my_images fliph flipv

通过首先将图像旋转90；然后水平翻转：

    python main.py ./my_images rot_90,fliph


##   
## Image Dict
main_dict.py文件
在该文件中可直接在pycharm等编辑器中调用，效果相仿，增加了部分操作。

    # 中心裁剪cropcen_300、随机裁剪cropran_400_2
| Code      | Description                      |Example Values|
|-----------|----------------------------------|------|
| `fliph`   | 水平翻转                             |`fliph`|
| `flipv`   | 垂直翻转                             |`flipv`|
| `noise`   | 随机噪声                             |`noise_0.01`,`noise_0.5`|
| `rot`     | 旋转角度(正为逆时针)                      |`rot_90`,`rot_-45`|
| `trans`   | 定量移动图像 (_x_y)                    |`trans_20_10`,`trans_-10_0`|
| `zoom`    | 放大/缩小指定区域                        |`zoom_0_0_20_20`,`zoom_-10_-20_10_10`|
| `blur`    | 模糊图像                             |`blur_1.5`|
| `cropcen` | 中心裁剪                             | `cropcen_300`    |
| `cropran`  | 随机裁剪<br/>(参数1：图片大小<br/>参数2：生成数量) | `cropran_400_2`     |

### 基本用法
在主函数中定义图片文件夹和需要进行的操作<br/>
操作：<br/>在同一个’‘下写多个操作（'flipv,fliph'）将对一张图片执行多个操作并保存一张图片，<br/>写多个’‘将对一张图片分别执行不同操作（'zoom_-145_-145_800_800', 'blur_0.5'）并保存多个图片
<br/>都用','间隔，例如：
    
        dir_op = ['F:\pythonProject\pretreatment\测试图片', 'zoom_-145_-145_800_800', 'blur_0.5', 'flipv,fliph']


##   
## Image Imgaug
main_imgaug.py文件
在该增强器中，调用imgaug库，实现更多操作。
单步、组合用法如下：

### 定义单步基本增强操作
    aug1 = iaa.Multiply(3.5)  # 所有像素与特定值相乘，更暗或更亮
    aug2 = iaa.MultiplyElementwise((0.5, 1.5))   # 将相邻像素的像素值乘以0.5-1.5随机不同的值，使每个像素更暗或更亮。
    aug3 = iaa.Affine(rotate=(0, 45))  # 随机旋转0-45度，rotate=45即旋转固定值45
    # (2,20)随机数值，4确定数值

### 定义复杂组合增强操作
    aug4 = iaa.OneOf([  # 应用其中的一个
        iaa.Affine(rotate=45),
        iaa.AdditiveGaussianNoise(scale=0.2 * 255),
        iaa.Add(50, per_channel=True),
        iaa.Sharpen(alpha=0.5)
    ])

    aug8 = iaa.Sequential([  # 按预定义顺序应用
        iaa.Affine(translate_px={"x": -40}),
        iaa.AdditiveGaussianNoise(scale=0.1 * 255)
    ])

    aug5 = iaa.SomeOf(2, [  # 随机应用其中的两个
        iaa.Affine(rotate=45),
        iaa.AdditiveGaussianNoise(scale=0.2 * 255),
        iaa.Add(50, per_channel=True),
        iaa.Sharpen(alpha=0.5)
    ], random_order=True)

    aug = iaa.SomeOf((0, None), [   # 应用给定的增强器中的零个到最大个
        iaa.Affine(rotate=45),
        iaa.AdditiveGaussianNoise(scale=0.2*255),
        iaa.Add(50, per_channel=True),
        iaa.Sharpen(alpha=0.5)
    ])

    aug6 = iaa.Sometimes(  # 高斯模糊应用于50％的图像的， 将仿射旋转和锐化应用到另外50％
        0.5,
        iaa.GaussianBlur(sigma=1.0),
        iaa.Sequential([iaa.Affine(rotate=45), iaa.Sharpen(alpha=1.0)])
    )
### 基本用法
确定文件路径

    # 图片文件相关路径
    inputpath = 'F:\pythonProject\pretreatment\测试图片'
单步增强操作只调用上方定义的操作，以‘，’分割，若使用多个增强对同一张图片进行操作，在列表中使用'（）'将操作组合
    
    # 将需要的增强操作放入一个列表中
    # 对一个图片多次操作，在列表中写入多个
    augmentations_list = [aug7, aug7, (aug2, aug3)]

更多解释参考：https://blog.csdn.net/lly1122334/article/details/88944589
<br/>imgaug官方说明：https://imgaug.readthedocs.io/en/latest/source/examples_basics.html

