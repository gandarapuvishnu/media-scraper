import os
import time
import urllib.request
from Common import Extractor, Downloader


def main():
    keywords = input("\nEnter key words to search for: ")
    extractor = Extractor('reddit')
    refs = extractor.get_web_page_links(keywords)

    path = './' + keywords + '/'
    if not os.path.isdir(path):
        os.mkdir(path)

    downloader = Downloader(path)

    start = time.time()
    for URL in refs:
        try:
            weburl = urllib.request.urlopen(URL)
            print('Result code: {}'.format(weburl.getcode()))
            data = str(weburl.read()).split()

            ext = '___'
            for i in data:
                if ('.jpg' in i) and ('https://' in i) and (('redd' in i) or ('imgur' in i)):
                    ext = 'jpg'
                if ('.png' in i) and ('https://' in i) and \
                        ((('redd' in i) or ('imgur' in i)) and 'redditstatic' not in i):
                    ext = 'png'

                link = i[i.index('https://'): i.index('.'+ext) + 4]
                downloader.download(link, ext)

        except Exception as z:
            print('Exception {}'.format(str(z)))
            pass

    end = time.time()
    print('\nTime spent downloading: {} seconds'.format(round(end - start), 1))


if __name__ == '__main__':
    main()