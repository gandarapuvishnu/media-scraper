
import os
import glob

if __name__ == '__main__':
    path = input('Path to media folder: ')

    # upload
    FilesExts = ['.jpg', '.jpeg', '.png', '.mp4', '.mkv']
    for ext in FilesExts:
        for file in glob.glob1(path, "*" + ext):
            os.system('telegram-upload --print-file-id ' + path + '/' + file)
            print("Uploading ", str(file), " to telegram..")


