import os
import time
import threading
from Common import Extractor, Downloader


def main():

    refs = extractor.get_web_page_links(keywords)
    print("Found ", len(refs), " websites")

    start = time.time()

    def fun(_url, _path):
        _imgs = extractor.get_all_images(_url)
        print('Extracted {} images from {}'.format(len(_imgs), url))
        for _img in _imgs:
            downloader.download(_img, _path)

    threads = []
    for url in refs:
        t = threading.Thread(target=fun, args=(url, folder))
        t.start()
        threads.append(t)

    for thread in threads:
        thread.join()

    end = time.time()
    print('\nTime spent downloading: {} seconds'.format(round(end - start), 1))


if __name__ == '__main__':
    keywords = input("\nEnter key words to search for: ")

    folder = './' + keywords
    try:
        os.mkdir(folder)
    except FileExistsError:
        pass

    extractor = Extractor()
    downloader = Downloader(folder)

    main()
