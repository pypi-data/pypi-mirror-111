#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author    : g1879
# @date      : 2021/5/30
# @email     : g1879@qq.com
# @File      : files.py
"""
    处理图片的常用方法

    经测试，openCV缩小后图片质量比PIL好
    但openCV写起来比较麻烦

    2019-10-23 by g1879

    注意：安装cv2语句是 pip install opencv-python
"""
from pathlib import Path
from shutil import copy
from typing import List, Union

from PIL import Image
from cv2 import imencode, imdecode, resize, INTER_AREA
from numpy import fromfile, uint8

from paths import get_usable_name


def get_imgs_list(path: str, ignore: Union[str, tuple, list] = None) -> List[Path]:
    """获取所有图片，返回Path对象列表
    :param path: 文件夹绝对路径
    :param ignore: 忽略的图片格式，如['.jpg']
    :return: 图片绝对路径列表
    """
    if isinstance(ignore, str):
        ignore = (ignore,)

    ignore = ignore or ()
    ignore = set(map(lambda x: x.lower() if x.startswith('.') else f'.{x}'.lower(), ignore))

    formats = {'.jpg', '.png', '.bmp', '.jpeg', '.gif'} - ignore

    return [x for x in Path(path).iterdir() if x.suffix.lower() in formats]


def img_to_jpg(path: str, del_src: bool = True) -> None:
    """将一个图片转为jpg格式
    :param path: 图片路径
    :param del_src: 是否删除原图片
    :return: None
    """
    img_file = Path(path)

    if img_file.suffix.lower() == '.jpg':
        return

    folder = img_file.parent
    base_name = get_usable_name(str(folder), f'{img_file.stem}.jpg')
    base_name = Path(base_name).stem

    img = Image.open(path)
    img = img.convert('RGB')
    img.save(f'{folder}\\{base_name}.jpg')

    # 删除不是jpg的图片
    if del_src:
        img_file.unlink()


def imgs_to_jpg(path: str, del_src: bool = True) -> None:
    """将传入路径中的所有图片转为jpg
    :param path: 存放图片的文件夹路径
    :param del_src: 是否删除原图片
    :return: None
    """
    imgs = get_imgs_list(path, ('.jpg',))

    # 执行转换
    for img_path in imgs:
        img_to_jpg(str(img_path), del_src)


def find_min_x(path: str, new_x: int = 800):
    """查看路径中是否有小于设定值宽度的图片，返回最小宽度"""
    imgs = get_imgs_list(path)
    for p in imgs:
        img = Image.open(p)
        x = img.size[0]

        if x < new_x:
            new_x = x

    return new_x


def zoom_img(path: str, new_x: int = None, new_y: int = None, rename: bool = False):
    """按照转入的xy值修改图片大小，如只传入一个值，保持图片比例缩放"""
    img = Path(path)
    folder_path = img.parent
    name = img.stem
    ext_name = img.suffix

    # 读取图像文件，因直接读取不支持中文路径，需要先读取为utf8再转码
    img = imdecode(fromfile(path, dtype=uint8), -1)
    y, x = img.shape[:2]

    # 根据传入的值生成新xy值
    if (not new_x and not new_y) or (new_x == x and new_y == y):
        return

    if new_x and not new_y:
        if x == new_x:
            return
        else:
            new_y = int(y * new_x / x)

    elif new_y and not new_x:
        if y == new_y:
            return
        else:
            new_x = int(x * new_y / y)

    new_img = resize(img, (new_x, new_y), interpolation=INTER_AREA)
    name = f'{name}_调整' if rename else name

    # 因不支持中文路径，保存也要用复杂的方式
    imencode(ext_name, new_img)[1].tofile(f'{folder_path}\\{name}{ext_name}')


def crop_img(path: Union[str, Path], lit_x: int = None, lit_y: int = None, img_name: str = None):
    """缩小图片，并保持内容的比例，裁剪超出的部分"""
    img = Path(path)
    file_name = img.stem
    dir_name = img.parent
    ext_name = img.suffix

    if img_name:
        to_path = f'{dir_name}\\{img_name}{ext_name}'
        copy(path, to_path)
    else:
        to_path = f'{dir_name}\\{file_name}{ext_name}'

    # 读取图像文件，获取xy值
    img = imdecode(fromfile(to_path, dtype=uint8), -1)
    y, x = img.shape[:2]

    lit_x = x if not lit_x else lit_x
    lit_y = y if not lit_y else lit_y

    if x == lit_x and y == lit_y:
        return

    # 根据比例，缩小图片
    if x / y <= lit_x / lit_y:
        zoom_img(to_path, new_x=lit_x)
    else:
        zoom_img(to_path, new_y=lit_y)

    # 读取缩小后的图片
    img = imdecode(fromfile(to_path, dtype=uint8), -1)
    y, x = img.shape[:2]

    # 根据比例，裁剪图片
    if x / y <= lit_x / lit_y:
        upper = (y - lit_y) // 2
        cropped = img[upper:upper + lit_y, 0:lit_x]  # 裁剪坐标为[y0:y1, x0:x1]
    else:
        left = (x - lit_x) // 2
        cropped = img[0:lit_y, left:left + lit_x]  # 裁剪坐标为[y0:y1, x0:x1]

    # 保存图片
    imencode(ext_name, cropped)[1].tofile(to_path)
