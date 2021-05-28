from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import os
import time
from urllib.parse import urljoin, urlparse
import requests
import urllib.request
from bs4 import BeautifulSoup as bs
from tqdm import tqdm
import pyautogui
import urllib.error


class Extractor:
    def __init__(self, param=''):
        print('Link Extractor')
        self.param = param

    def check(self, plink):
        if str(plink).find(self.param) == -1:
            return False
        else:
            return True

    def get_web_page_links(self, key):
        driver = webdriver.Chrome()
        driver.get('https://google.com/')
        print("\nOpening Chrome")
        time.sleep(2)

        searchbox = driver.find_element_by_name('q')
        key += ' {}'.format(self.param)
        searchbox.send_keys(key)
        searchbox.send_keys(Keys.ENTER)

        time.sleep(1)
        pyautogui.keyDown('esc')
        pyautogui.keyUp('esc')

        _refs = []
        page_num = 0
        while True:
            page_num += 1
            try:
                print("\nNavigating to Page " + str(page_num))
                links = driver.find_elements_by_class_name('yuRUbf')
                count = 0
                for link in links:
                    plink = link.find_element_by_tag_name('a').get_attribute("href")
                    if is_valid(plink):
                        if self.check(plink):
                            print(str(link.find_element_by_tag_name('a').get_attribute("href")))
                            _refs.append(str(link.find_element_by_tag_name('a').get_attribute("href")))
                            count += 1

                if count > 0:
                    print("Found " + str(count) + ' {} web pages in page '.format(self.param) + str(page_num))
                else:
                    print('No {} web pages found in page '.format(self.param) + str(page_num))
                _next = driver.find_element_by_xpath('//*[@id="pnnext"]')
                _next.click()
                time.sleep(1)
            except NoSuchElementException:
                print("Last page reached\n")
                break
        driver.close()
        return _refs

    def get_all_images(self, url):
        """
        Returns all image URLs on a single `url`
        """
        soup = bs(requests.get(url).content, "html.parser")
        urls = []
        for img in tqdm(soup.find_all("img"), "Extracting images"):
            img_url = img.attrs.get("src")
            if not img_url:
                # if img does not contain src attribute, just skip
                continue
            # make the URL absolute by joining domain with the URL that is just extracted
            img_url = urljoin(url, img_url)
            # remove URLs like '/hsts-pixel.gif?c=3.2.5'
            try:
                pos = img_url.index("?")
                img_url = img_url[:pos]
            except ValueError:
                pass
            # finally, if the url is valid
            if is_valid(img_url):
                urls.append(img_url)
        return urls


def is_valid(url):
    """
    Checks whether `url` is a valid URL.
    """
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)


def scroll(driver, X=3, _wait=10, _sleep=2):
    value = 0
    print('Scrolling...')
    for i in range(X):
        driver.execute_script("scrollBy(" + str(value) + ",+1000);")
        value += _wait
        time.sleep(_sleep)
    # The above code is just to scroll down the page for loading all images


class Downloader:
    def __init__(self, pathname):
        print('Download images')
        self.pathname = pathname
        self.cnt = 0

    def download(self, url, FORMAT):
        """
        Downloads a file given an URL and puts it in the folder `pathname`
        """
        # if path doesn't exist, make that path dir
        if not os.path.isdir(self.pathname):
            os.makedirs(self.pathname)
        # download the body of response by chunk, not immediately
        try:
            response = requests.get(url, stream=True)
        except requests.exceptions.ConnectionError:
            time.sleep(10)
            response = requests.get(url, stream=True)

        # get the total file size
        file_size = int(response.headers.get("Content-Length", 0))

        # get the file name
        self.cnt += 1
        filename = os.path.join(self.pathname, 'image-{}.{}'.format(FORMAT, self.cnt))

        # progress bar, changing the unit to bytes instead of iteration (default by tqdm)
        progress = tqdm(response.iter_content(1024), f"Downloading {filename}", total=file_size, unit="B",
                        unit_scale=True,
                        unit_divisor=1024)
        with open(filename, "wb") as f:
            for data in progress:
                # write data read to the file
                f.write(data)
                # update the progress bar manually
                progress.update(len(data))

    def write(self, src, dest):
        try:
            urllib.request.urlretrieve(url=src, filename=dest)
        except urllib.error.HTTPError:
            print("HTTPError at {}".format(src))


if __name__ == '__main__':
    print('new main.')
