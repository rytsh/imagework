# Image Processing Lesson
__Eray Ates__

With this homework, I use __python3__ and _ImageMagick_ binding library called __Wand__.

First we need to download requirement.

> Check this link for more information about Wand.
> http://docs.wand-py.org/en/0.5.3/
> https://buildmedia.readthedocs.org/media/pdf/wand/latest/wand.pdf

## Install

libmagickwand-dev or magicwand library download with your package manager.

If you run directly with python, you should have libtk for plot.

## Usage

In this homework, we should do get lena 256x256 color image. I use this link:
>http://andrewd.ces.clemson.edu/images/ppm/lena256.ppm

If you install imagemagick on your system, you will get identify command. With use this command you can get list of compatible image formats. If you want to edit some formats you need to install specific libraries.
```shell
identify -list format
```

Install requirements
```shell
sudo python3 -m pip install -r requiremens.txt
```

Run
```shell
python image.py
```

and check `out` folder

## Customization

Edit config.ini file to use another image.