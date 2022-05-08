#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PIL import Image
import numpy as np

image_file = 'ycbcr.jpg' 

if __name__ == '__main__':
    im = Image.open(image_file)    #打开图像文件
    im = im.convert('YCbCr')       #将原图像转化为灰度图
    w, h = im.size                 
    y_array = np.zeros((w, h), 'uint8') 
    cb_array = np.zeros((w, h), 'uint8') 
    cr_array = np.zeros((w, h), 'uint8') 
    for i in range(w):             
        for j in range(h):
            y_array[i][j] = im.getpixel((i, j))[0]
            cb_array[i][j] = im.getpixel((i, j))[1]
            cr_array[i][j] = im.getpixel((i, j))[2]


    y_array = y_array.transpose()            
    cb_array = cb_array.transpose()
    cr_array = cr_array.transpose()

    Image.fromarray(y_array).save("y_" + image_file) 
    Image.fromarray(cr_array).save("cr_" + image_file) 
    Image.fromarray(cb_array).save("cb_" + image_file)
