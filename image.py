#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 25 14:14:05 +03 2019.

Image Processing Lesson
@author: Eray Ates
"""

import os
import urllib.request
import numpy as np
import matplotlib.pyplot as plt
import configparser

from wand.image import Image
from wand.display import display

config = configparser.ConfigParser()


def createFolders(folders):
    """Create folders of out and assets."""
    for folder in folders:
        if not os.path.isdir(folder):
            os.mkdir(folder)


def downloadImage(img_url, folder, img_name):
    """Url download."""
    if not os.path.isfile("{}/{}".format(folder, img_name)):
        print("Downloading img_name..")
        urllib.request.urlretrieve(img_url, "{}/{}".format(folder, img_name))


def greyScale(img):
    """Grey scale of image."""
    array = np.zeros([img.height, img.width, 1], dtype=np.uint8)

    # Get RGB values of every pixel and 2D location
    for row, rown in zip(img, range(img.height)):
        for col, coln in zip(row, range(img.width)):
            x = int((col.red_int8 + col.green_int8 + col.blue_int8) / 3)
            array[rown][coln] = [x]

    return array


def threshold(array_img):
    """Get threshold value."""
    threshold_value = int(np.mean(array_img.ravel()))
    return threshold_value


def pixel2image(array_img, out, iname, img_name):
    """Pixel to image."""
    with Image.from_array(array_img) as img_x:
        # this line will wait you to close displayed image
        # display(img_x)
        img_x.format = 'png'
        img_x.save(filename='{}/{}-{}.{}'.format(out, os.path.splitext(img_name)[0], iname, img_x.format))


if __name__ == "__main__":
    config.read('config.ini')

    img_url = config['MAIN']['image']

    folder_content = config['MAIN']['folder']
    folder_out = config['MAIN']['out']

    img_name = os.path.basename(img_url)
    createFolders((folder_content, folder_out))
    downloadImage(img_url, folder_content, img_name)

    asset_org = "{}/{}".format(folder_content, img_name)
    asset_out = "{}/{}".format(folder_out, img_name)

    with Image(filename=asset_org, format=os.path.splitext(img_name)[1][1:]) as img:
        # print(img.size)
        # Transfer to grey and return as array of pixel
        array = greyScale(img)

        # pixel to image
        pixel2image(array, folder_out, 'grey', img_name)

        # Histogram save
        plt.style.use('classic')
        plt.hist(array.ravel(), 256, [0, 256], color='black')
        plt.savefig('{}/{}-histogram.png'.format(folder_out, os.path.splitext(img_name)[0]))

        # Find threshold
        threshold_value = threshold(array)

        # Apply that threshold value
        # Save original value
        array_the = array.copy()

        array_the[array_the >= threshold_value] = 255
        array_the[array_the < threshold_value] = 0

        # pixel to image
        pixel2image(array_the, folder_out, 'threshold', img_name)
