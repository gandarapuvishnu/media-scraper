from selenium import webdriver
import time
from downloadImages.Common import Extractor, scroll, Downloader
import os


def get_pins(link):
    def reach_for_highest_resolution(srt):
        return srt[:21] + 'originals' + srt[21 + srt[21:].index('/'):]

    wait = 4000
    sleep = 2
    print('\nOpening ' + str(link))
    gldriver = webdriver.Chrome()
    time.sleep(2)
    gldriver.get(link)

    scroll(gldriver, 10, wait, sleep)

    elem1 = gldriver.find_elements_by_class_name('GrowthUnauthPinImage__Image')
    sub = []
    for i in elem1:
        sub.append(i.get_attribute('src'))

    count = 0
    downloader = Downloader(keywords)

    print("Found " + str(len(sub)) + ' images\n')
    for sr in sub:
        src = str(sr)

        dest = keywords + '/image' + str(count) + '.jpg'
        try:
            src = reach_for_highest_resolution(src)
        except Exception as e:
            print("\nTried for original resolution..failed with Exception.: " + str(e))
        count += 1
        downloader.write(src, dest)


def main(keywords):
    extractor = Extractor('pinterest')
    refs = extractor.get_web_page_links(keywords)
    print("Found " + str(len(refs)) + ' web pages\n')

    try:
        os.mkdir(keywords)
    except FileExistsError:
        pass

    for url in refs:
        get_pins(url)
        time.sleep(3)


if __name__ == '__main__':
    keys = input("\nEnter key words to search for: ")
    main(keys)
