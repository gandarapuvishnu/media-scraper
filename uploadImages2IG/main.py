
import glob
import time
import threading

from uploadImages2IG.preUmain import tojpg, login, upload

from colorama import init, Fore, Style

# essential for Windows environment
init()


def cprint(s, color=Fore.YELLOW, brightness=Style.BRIGHT, **kwargs):
    """Utility function wrapping the regular `print()` function
    but with colors and brightness"""
    print(f"{brightness}{color}{s}{Style.RESET_ALL}", **kwargs)


def main(path):
    # 2. Get credentials
    user = input("Enter instagram username: ")
    pas = input("Enter instagram password: ")

    # 3. Login
    try:
        login(user, pas)
        cprint("Login successful.")
    except KeyError:
        cprint("Incorrect credentials")
        exit()

    start_time = time.time()
    # 4. Convert all images to jpg-format
    tojpg(path)
    cprint("All images converted to jpg format.")

    img_files = glob.glob(path + '\*.jpg')

    count = 1
    threads = []

    # 5. resize to instagram size-format
    # 6. Upload
    cprint("Uploading {} jpg files".format(len(img_files)))
    for i, link in enumerate(img_files):
        t = threading.Thread(target=upload, args=(str(link), 'Uploaded by Python'))
        t.start()
        threads.append(t)

    for thread in threads:
        thread.join()
        cprint("Uploaded {} / {}\n".format(count, len(threads)))
        count += 1

    last_time = time.time()
    cprint("Time elapsed: {} seconds".format(round(last_time - start_time, 1)))


if __name__ == '__main__':
    # 1. Get Folder path
    main(input("Enter folder path: "))