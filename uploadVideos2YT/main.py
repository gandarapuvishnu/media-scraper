import os
import time
import glob


def main(_title, filename):
    title = _title
    etp = time.time()
    cmd = 'python upload.py --file ' + filename + ' --title ' + title

    os.system(cmd)

    etp -= time.time()

    print("Time taken to upload: ", round(abs(etp), 2), 'seconds')


if __name__ == '__main__':

    path = input('Enter folder path: ')

    # Get all mp4 files from path
    files = glob.glob1(path, '*.mp4')

    for f in files:
        print('\n' + os.path.join(path, f))
        Title = str(f)

        main(_title=Title, filename=os.path.join(path, f))
