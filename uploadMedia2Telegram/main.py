
import os
import glob

from colorama import init, Fore, Style

# essential for Windows environment
init()


def cprint(s, color=Fore.CYAN, brightness=Style.NORMAL, **kwargs):
    """Utility function wrapping the regular `print()` function
    but with colors and brightness"""
    print(f"{brightness}{color}{s}{Style.RESET_ALL}", **kwargs)


def main(path):
    # upload
    FilesExts = ['.jpg', '.jpeg', '.png', '.mp4', '.mkv']
    for ext in FilesExts:
        Files = glob.glob1(path, "*" + ext)
        for i, file in enumerate(Files):
            cprint("\nUploading {} / {}".format(i+1, len(Files)))
            os.system('telegram-upload --print-file-id ' + path + '/' + file)


if __name__ == '__main__':
    folder = input('Path to media folder: ')

    main(folder)


