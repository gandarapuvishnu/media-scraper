
from downloadImages.ImageDownloaderFromPinterest import main as pinImgs
from downloadImages.ImageDownloaderFromGoogleImages import main as googleImgs
from downloadImages.ImageDownloaderFromWebPages import main as webImgs
from downloadImages.ImageDownloaderFromReddit import main as redImgs
from uploadFiles2Gdrive.main import upload_files as gdrive
from uploadImages2IG.main import main as ig
from uploadMedia2Telegram.main import main as tel

import sys
import os


def download_images(keywords):
    # Directly downloads relevant google images to the folder created.
    googleImgs(keywords)

    # Directly downloads relevant images obtained from various web pages.
    webImgs(keywords)

    # Directly downloads relevant pinterest images to the folder.
    pinImgs(keywords)

    # Directly downloads relevant reddit images to the folder.
    redImgs(keywords)


def upload_images(keywords):
    path = './' + keywords

    if os.path.isdir(path):
        # Uploads images from the folder, into google drive with same folder name -
        # Google cloud account OAuth handle required
        gdrive(path, keywords)

        # Uploads all images to telegram (Saved Messages) - API id required
        tel(path)

        # uploads images to Instagram - Login creds required
        ig(path)
    else:
        sys.exit(1)


if __name__ == '__main__':
    print("Hello World")

    keys = input("\nEnter key words to search for: ")

    download_images(keys)

    upload_images(keys)
