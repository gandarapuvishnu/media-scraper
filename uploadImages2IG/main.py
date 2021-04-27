
import glob
import time
import threading

from preUmain import log, tojpg, login, upload


if __name__ == '__main__':
    log("Hello World")

    # 1. Get Folder path
    path = input("Enter folder path: ")

    # 2. Get credentials
    user = input("Enter instagram username: ")
    pas = input("Enter instagram password: ")

    # 3. Login
    try:
        login(user, pas)
        log("Login successful.")
    except KeyError:
        log("Incorrect credentials")
        exit()

    start_time = time.time()
    # 4. Convert all images to jpg-format
    tojpg(path)
    log("All images converted to jpg format.")

    img_files = glob.glob(path + '\*.jpg')

    count = 1
    threads = []

    # 5. resize to instagram size-format
    # 6. Upload
    log("Uploading {} jpg files".format(len(img_files)))
    for i, link in enumerate(img_files):
        t = threading.Thread(target=upload, args=(str(link), 'Uploaded by Python'))
        t.start()
        threads.append(t)

    for thread in threads:
        thread.join()
        log("Uploaded {} / {}\n".format(count, len(threads)))
        count += 1

    last_time = time.time()
    log("Time elapsed: {} seconds".format(round(last_time-start_time, 1)))
