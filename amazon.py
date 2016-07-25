# -*- coding: utf-8 -*-
# Created by Chuande Wang on 16/6/15

import os
import sys
import traceback
from PIL import Image


TEXTCOLOR = 0
BACKCOLOR = 255


def SplitCharacter(Block):
    '''根据平均字符宽度找极小值点分割字符'''
    Pixels = Block.load()
    (Width, Height) = Block.size
    MaxWidth = 20 # 最大字符宽度
    MeanWidth = 14    # 平均字符宽度
    if Width < MaxWidth:  # 若小于最大字符宽度则认为是单个字符
        return [Block]
    Blocks = []
    PixelCount = []
    for i in xrange(Width):  # 统计竖直方向像素个数
        Count = 0
        for j in xrange(Height):
            if Pixels[i, j] == TEXTCOLOR:
                Count += 1
        PixelCount.append(Count)

    for i in xrange(Width):  # 从平均字符宽度处向两侧找极小值点，从极小值点处进行分割
        if MeanWidth - i > 0:
            if PixelCount[MeanWidth - i - 1] > PixelCount[MeanWidth - i] < PixelCount[MeanWidth - i + 1]:
                Blocks.append(Block.crop((0, 0, MeanWidth - i + 1, Height)))
                Blocks += SplitCharacter(Block.crop((MeanWidth - i + 1, 0, Width, Height)))
                break
        if MeanWidth + i < Width - 1:
            if PixelCount[MeanWidth + i - 1] > PixelCount[MeanWidth + i] < PixelCount[MeanWidth + i + 1]:
                Blocks.append(Block.crop((0, 0, MeanWidth + i + 1, Height)))
                Blocks += SplitCharacter(Block.crop((MeanWidth + i + 1, 0, Width, Height)))
                break
    print(Blocks)
    return Blocks


#!python
def SplitPicture(Picture):
    '''用连通区域法初步分隔'''
    Pixels = Picture.load()
    (Width, Height) = Picture.size

    xx = [0, 1, 0, -1, 1, 1, -1, -1]
    yy = [1, 0, -1, 0, 1, -1, 1, -1]

    Blocks = []

    for i in xrange(Width):
        for j in xrange(Height):
            if Pixels[i, j] == BACKCOLOR:
                continue
            #Pixels[i, j] = TEMPCOLOR
            Pixels[i, j] = TEXTCOLOR
            MaxX = 0
            MaxY = 0
            MinX = Width
            MinY = Height

            # BFS算法从找(i, j)点所在的连通区域
            Points = [(i, j)]
            for (x, y) in Points:
                for k in xrange(8):
                    if 0 <= x + xx[k] < Width and 0 <= y + yy[k] < Height and Pixels[x + xx[k], y + yy[k]] == TEXTCOLOR:
                        MaxX = max(MaxX, x + xx[k])
                        MinX = min(MinX, x + xx[k])
                        MaxY = max(MaxY, y + yy[k])
                        MinY = min(MinY, y + yy[k])
                        #Pixels[x + xx[k], y + yy[k]] = TEMPCOLOR
                        Pixels[x + xx[k], y + yy[k]] = TEXTCOLOR
                        Points.append((x + xx[k], y + yy[k]))

            TempBlock = Picture.crop((MinX, MinY, MaxX + 1, MaxY + 1))
            TempPixels = TempBlock.load()
            BlockWidth = MaxX - MinX + 1
            BlockHeight = MaxY - MinY + 1
            for y in xrange(BlockHeight):
                for x in xrange(BlockWidth):
                    #if TempPixels[x, y] != TEMPCOLOR:
                    if TempPixels[x, y] != TEXTCOLOR:
                        TempPixels[x, y] = BACKCOLOR
                    else:
                        TempPixels[x, y] = TEXTCOLOR
                        Pixels[MinX + x, MinY + y] = BACKCOLOR
            TempBlocks = SplitCharacter(TempBlock)
            for TempBlock in TempBlocks:
                Blocks.append(TempBlock)

    print(Blocks)
    return Blocks



def binarized(filename):
    #存放训练数据
    if not os.path.exists('training'):
        os.mkdir('training')

    #网络上的图片转换成Image对象
    image = Image.open(filename)
    #灰度化处理
    #有很多种算法，这里选择rgb加权平均值算法
    gray_image = Image.new('RGB', image.size)
    #获得rgb数据序列，每一个都是(r,g,b)三元组
    # raw_data = image.getdata()
    width, height  = image.size
    rgb_im = image.convert('RGB')


    for x in range(width):
        for y in range(height):
            r, g, b = rgb_im.getpixel((x, y))
            #print(r,g,b)
            value = 0.299 * r + 0.587 * g + 0.114 * b
            if value < 5:
                gray_image.putpixel((x, y), (0, 0, 0))
            else:
                gray_image.putpixel((x, y), (255, 255, 255))

    gray_image.save('test.jpg')
    image.close()
    gray_image.close()


def main(image_name):
    print('start')
    print(image_name)
    try:
        img = Image.open(image_name)
    except Exception:
        print(traceback.format_exc())

    print("before SplitPicture")

    SplitPicture(img)








if __name__ == '__main__':
    image_name = sys.argv[1]
    main(image_name)