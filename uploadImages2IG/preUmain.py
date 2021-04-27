
from instabot import Bot
from PIL import Image
import PIL.Image
import numpy as np
import os
import glob
import shutil
import tempfile
import string
import random


def log(msg):
    _file = open('log.txt', 'a')
    _file.write(msg+'\n')
    print(msg)
    _file.close()


if os.path.isdir('./config'):
    shutil.rmtree('./config')
    log("Config cleared.")

if os.path.isfile('./log.txt'):
    os.remove('./log.txt')
    log("Log cleared.")

bot = Bot()


def _entropy(data):
    """Calculate the entropy of an image"""
    hist = np.array(PIL.Image.fromarray(data).histogram())
    hist = hist / hist.sum()
    hist = hist[hist != 0]
    return -np.sum(hist * np.log2(hist))


def crop(x, y, data, w, h):
    x = int(x)
    y = int(y)
    return data[y: y + h, x: x + w]


def crop_maximize_entropy(img, min_ratio=4 / 5, max_ratio=90 / 47):
    from scipy.optimize import minimize_scalar

    w, h = img.size
    data = np.array(img)
    ratio = w / h
    if ratio > max_ratio:  # Too wide
        w_max = int(max_ratio * h)

        def _crop(x):
            return crop(x, y=0, data=data, w=w_max, h=h)

        xy_max = w - w_max
    else:  # Too narrow
        h_max = int(w / min_ratio)

        def _crop(y):
            return crop(x=0, y=y, data=data, w=w, h=h_max)

        xy_max = h - h_max

    to_minimize = lambda xy: -_entropy(_crop(xy))
    x = minimize_scalar(to_minimize, bounds=(0, xy_max), method="bounded").x
    return PIL.Image.fromarray(_crop(x))


def strip_exif(img):
    """Strip EXIF data from the photo to avoid a 500 error."""
    data = list(img.getdata())
    image_without_exif = PIL.Image.new(img.mode, img.size)
    image_without_exif.putdata(data)
    return image_without_exif


def correct_ratio(photo):
    from instabot.api.api_photo import compatible_aspect_ratio, get_image_size

    return compatible_aspect_ratio(get_image_size(photo))


def prepare_and_fix_photo(photo):
    N = 8
    with open(photo, "rb") as f:
        img = PIL.Image.open(f)
        img = strip_exif(img)
        if not correct_ratio(photo):
            img = crop_maximize_entropy(img)

        res = ''.join(random.choices(string.ascii_lowercase, k=N))
        photo = os.path.join(tempfile.gettempdir(), res + ".jpg")
        img.save(photo)
    return photo


def login(user, pas):
    bot.login(username=user, password=pas)


def upload(img, caption):
    try:
        bot.upload_photo(prepare_and_fix_photo(img), caption)
    except Exception as e:
        log(str(e))
        log("Failed to upload {}\n".format(img))
        pass


def tojpg(filepath):

    exts = ['.jpeg', '.png']
    for ext in exts:
        files = glob.glob(filepath + '\*' + ext)
        # Rename
        for file in files:
            im = Image.open(file)
            rgb_im = im.convert('RGB')
            rgb_im.save(file.replace(ext[1:], "jpg"), quality=95)
        # Delete duplicates
        for f in files:
            os.remove(f)
