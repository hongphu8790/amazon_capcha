#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Chuande Wang on 16/6/17

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Chuande Wang on 16/6/15
import sys
import os
import StringIO
import urllib
import pytesseract
from PIL import Image

def tesseract_image(image):
    return pytesseract.image_to_string(image, config='-psm 10', lang='image')



#图片x轴的投影，如果有数据（黑色像素点）值为1否则为0
def get_projection_x(image):
    p_x = [0 for x in xrange(image.size[0])]
    for w in xrange(image.size[0]):
        for h in xrange(image.size[1]):
            #print(image.getpixel((h,w)))
            if image.getpixel((w,h)) == 0:
                p_x[w] = 1
    return p_x

#获取分割后的x轴坐标点
#返回值为[起始位置, 长度] 的列表
def get_split_seq(projection_x):
    res = []
    for idx in xrange(len(projection_x) - 1):
        p1 = projection_x[idx]
        p2 = projection_x[idx + 1]
        if p1 == 1 and idx == 0:
            res.append([idx, 1])
        elif p1 == 0 and p2 == 0:
            continue
        elif p1 == 1 and p2 == 1:
            res[-1][1] += 1
        elif p1 == 0 and p2 == 1:
            res.append([idx + 1, 1])
        elif p1 == 1 and p2 == 0:
            continue
    return res

#分割后的图片，x轴分割后，同时去掉y轴上线多余的空白
def split_image(image, split_seq=None):

    if split_seq is None:
        split_seq = get_split_seq(get_projection_x(image))
    length = len(split_seq)
    imgs = [[] for i in xrange(length)]
    res = []
    for w in xrange(image.size[1]):
        line = [image.getpixel((h,w)) for h in xrange(image.size[0])]
        for idx in xrange(length):
            pos = split_seq[idx][0]
            llen = split_seq[idx][1]
            l = line[pos:pos+llen]
            imgs[idx].append(l)
    for idx in xrange(length):
        datas = []
        height = 0
        for data in imgs[idx]:
            flag = False
            for d in data:
                if d == 0:
                    flag = True
            if flag == True:
                height += 1
                datas += data
        child_img = Image.new('L',(split_seq[idx][1], height))
        child_img.putdata(datas)
        res.append(child_img)

    #print(type(res))
    #print(res)
    return res


def binarized(image_buffer):
    #网络上的图片转换成Image对象
    image = Image.open(StringIO.StringIO(image_buffer))
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


    image.close()
    #print(type(gray_image))
    #print(gray_image)
    image_word_list = split_image(gray_image)
    word_list = []
    for word in image_word_list:
        sigle_word = tesseract_image(word)
        word_list.append(sigle_word)
    word_string = ''.join(word_list)
    #print word_string
    return  word_string




def main(filename):
    root, dirs, files = os.walk(filename)
    for name in files:
        print(os.path.abspath(name))
    #binarized(filename)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        exit('Usage: amazon_capcha url')
    if len(sys.argv) == 2:
        url = sys.argv[1]
        binarized(url)

