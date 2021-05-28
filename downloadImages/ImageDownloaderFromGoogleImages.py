from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os
from Common import Downloader


def main():
    driver = webdriver.Chrome()

    try:
        os.mkdir(name_of_folder)
    except FileExistsError:
        pass
    time.sleep(2)

    # Search and locate them
    driver.get('https://www.google.com/')
    searchBox = driver.find_element_by_name('q')
    searchBox.send_keys(keywords)
    searchBox.send_keys(Keys.ENTER)
    elem = driver.find_element_by_link_text('Images')
    elem.get_attribute('href')
    elem.click()

    # Scroll to load images
    value = 0
    for i in range(20):
        wait = 400
        driver.execute_script("scrollBy(" + str(value) + "," + str(wait) + ");")
        value += wait
        time.sleep(2)

    elem1 = driver.find_element_by_id('islmp')
    sub = elem1.find_elements_by_tag_name("img")
    # Google images contain in a div tag with is ‘islmp’. That’s the reason to fetch it.

    print(f'Found {len(sub)} images')
    print('Downloading..')
    # Download
    for (i, link) in enumerate(sub):
        try:
            src = str(link.get_attribute('src'))
            dest = name_of_folder + '/image' + str(i + 1) + '.png'
            downloader.write(src, dest)
        except:
            pass

    driver.close()


if __name__ == '__main__':
    keywords = input("Input: ")

    name_of_folder = './' + keywords
    try:
        os.mkdir(name_of_folder)
    except FileExistsError:
        pass

    downloader = Downloader(name_of_folder)

    main()
