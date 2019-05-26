#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 25 14:14:05 +03 2019.

Image Processing Lesson's Homeworks
Author: Eray Ates
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


# def greyScale(img):
#     """Grey scale of image."""
#     array = np.zeros([img.height, img.width, 1], dtype=np.uint8)

#     # Get RGB values of every pixel and 2D location
#     for row, rown in zip(img, range(img.height)):
#         for col, coln in zip(row, range(img.width)):
#             x = int((col.red_int8 + col.green_int8 + col.blue_int8) / 3)
#             array[rown][coln] = [x]

#     return array


def img2array(img, color="Default"):
    """Get pixels."""
    color_mode = {
        'RGB': 3,
        'BW': 1,
        'Default': 3,
    }

    color = color if color in color_mode else 'Default'

    array = np.zeros([img.height, img.width, color_mode[color]], dtype=np.uint8)

    # Get RGB values of every pixel and 2D location
    for row, rown in zip(img, range(img.height)):
        for col, coln in zip(row, range(img.width)):
            if 1 == color_mode[color]:
                x = [int((col.red_int8 + col.green_int8 + col.blue_int8) / 3)]
            else:
                x = [col.red_int8, col.green_int8, col.blue_int8]

            array[rown][coln] = x

    return array


def array2grey(array_img):
    """Array to grey."""
    return np.mean(array_img, axis=2, keepdims=1, dtype=np.uint16).astype(np.uint8)


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


def screenLog(message, title="INFO"):
    """Print to Log Screen."""
    print("[{0}] \t==\t {1} {2}".format(title, message, (60 - len(message)) * "="))


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

    # HW1 Part
    if config['HOMEWORKS'].getboolean('HW1'):
        screenLog("Homework 1 started")
        screenLog("Transfering image to array as grey", "HW1")
        with Image(filename=asset_org, format=os.path.splitext(img_name)[1][1:]) as img:
            # Transfer opened img to array
            array = img2array(img, color="BW")

        # pixel to image
        screenLog("Saving grey image", "HW1")
        pixel2image(array, folder_out, 'grey', img_name)

        # Histogram save
        screenLog("Generating histogram", "HW1")
        plt.style.use('classic')
        plt.hist(array.ravel(), 256, [0, 256], color='black')
        plt.savefig('{}/{}-histogram.png'.format(folder_out, os.path.splitext(img_name)[0]))

        # Find threshold
        screenLog("Finding threshold", "HW1")
        threshold_value = threshold(array)

        # Apply that threshold value
        # Save original value
        array_the = array.copy()

        array_the[array_the >= threshold_value] = 255
        array_the[array_the < threshold_value] = 0

        # pixel to image
        screenLog("Saved applied threshold value", "HW1")
        pixel2image(array_the, folder_out, 'threshold', img_name)

    # HW2 Part
    if config['HOMEWORKS'].getboolean('HW2'):
        screenLog("Homework 2 started")
        screenLog("Transfering image to array as 3 color", "HW2")
        with Image(filename=asset_org, format=os.path.splitext(img_name)[1][1:]) as img:
            # Transfer opened img to array
            img_height, img_width = img.size
            array = img2array(img, color="RGB")

        # Generate 256x256 zero mean Gaussion noises
        screenLog("Generating gaussion noises and appling", "HW2")
        sigma = [1, 5, 10, 20]  # standard deviation
        mu = 0  # mean

        for i in sigma:
            screenLog("Using standard deviation {} and saving image".format(i), "HW2")
            s = np.random.normal(mu, i, size=(img_height, img_width, 1)).astype(np.int8)

            # plt.style.use('classic')
            # plt.hist(s.ravel(), 256, [- 80, 80], color='black')
            # plt.savefig('{}/{}-noise-histogram.png'.format(folder_out, os.path.splitext(img_name)[0]))

            # Add this noises to image
            array_the = np.add(array, s, dtype=np.int16)
            array_the[array_the > 255] = 255
            array_the[array_the < 0] = 0
            array_the = array_the.astype(np.uint8)

            # pixel to image
            pixel2image(array_the, folder_out, 'noise-{}-C'.format(i), img_name)

            # turn greyscale of that array
            pixel2image(array2grey(array_the), folder_out, 'noise-{}-B'.format(i), img_name)
