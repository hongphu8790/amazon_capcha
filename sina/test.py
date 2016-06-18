#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Chuande Wang on 16/6/15
import sys
import os
from PIL import Image



def binarized(filename):
    print filename

    #存放训练数据
    if not os.path.exists('training_amazon'):
        os.mkdir('training_amazon')

    print filename
    #网络上的图片转换成Image对象
    image = Image.open(filename)
    #灰度化处理
    #有很多种算法，这里选择rgb加权平均值算法
    #gray_image = Image.new('RGB', image.size)
    gray_image = Image.new('1', image.size)
    #获得rgb数据序列，每一个都是(r,g,b)三元组
    # raw_data = image.getdata()
    width, height  = image.size
    # rgb_im = image.convert('RGB')
    raw_data = image.load()


    for x in range(width):
        for y in range(height):
            value = raw_data[x, y]
            if value < 6:
                gray_image.putpixel((x, y), 0)
            else:
                gray_image.putpixel((x, y), 255)
    img_name = os.path.basename(filename).split('.')[0]
    print(img_name)
    gray_image.save(os.path.join('training_amazon', '%s.png' %img_name))
    image.close()
    gray_image.close()


def show_image_pixel(filename):
    img = Image.open(filename)
    pixels = img.load()

    for i in range(img.size[0]):  # for every pixel:
        for j in range(img.size[1]):
            print("****")
            print(pixels[i, j])
            #pixels[i, j] = (i, j, 100)  # set the colour accordingly



def main(filename):
    root, dirs, files = os.walk(filename)
    for name in files:
        print(os.path.abspath(name))
    #binarized(filename)


if __name__ == '__main__':
    # if len(sys.argv) < 2:
    #     exit('Usage: test.py dirname')
    # if len(sys.argv) == 2:
    #     dirname = sys.argv[1]
    #     if os.i
    #     main(dirname)
    rootDir = "amazonpicture"
    for root, dirs, files in os.walk(rootDir):
        for name in files:
            image_name = os.path.join(root, name)
            #print image_name
            binarized(image_name)