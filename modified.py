import urllib
import re
from lxml import etree
import random


class Downloader():
    '''
    Class to retreive HTML code
    and binary files from a
    specific website
    '''

    def __init__(self, url):
        self.url = url
        self.contents = ''

    def download(self, image_name='', is_image=False):
        browser = urllib.urlopen(self.url)
        response = browser.getcode()
        if response == 200:
            self.contents = browser.read()

        if is_image:
            image_file = open(image_name, 'wb')
            image_file.write(self.contents)
            image_file.close()


class xkcdParser(Downloader):
    '''
    Class for parsing xkcd.com
    '''

    def __init__(self, url):
            Downloader.__init__(self, url)
            self.last_comic_nr = None
            self.title = ''
            self.caption = ''

    def get_last_comic_nr(self):
        try:
            self.last_comic_nr = re.search(r"http://xkcd.com/(\d+)", self.contents).group(1)
            self.last_comic_nr = int(self.last_comic_nr)
        except:
            self.last_comic_nr = None

    def get_current_comic(self):
        self.download(self.url)
        self.get_last_comic_nr()
        self.get_title()
        self.get_caption()
        self.get_comic()

    def get_random_comic(self):
        if self.last_comic_nr:
            comic_nr = random.randint(1, self.last_comic_nr)
            self.url = "http://xkcd.com/" + str(comic_nr)
            self.download()
            self.get_title()
            self.get_caption()
            self.get_comic()

    def get_title(self):
        if self.contents:
            tree = etree.HTML(self.contents)
            self.title = tree.xpath("string(//div[@id='ctitle'])")

    def get_caption(self):
        if self.contents:
            tree = etree.HTML(self.contents)
            self.caption = tree.xpath("string(//div[@id='comic']/img/@title)")

    def get_comic(self):
        if self.contents:
            tree = etree.HTML(self.contents)
            self.url = tree.xpath("string(//div[@id='comic']/img/@src)")
            self.download(self.title, is_image=True)


if __name__ == '__main__':
    url = "http://xkcd.com/"
    xkcd_parser = xkcdParser(url)
    xkcd_parser.get_current_comic()
    xkcd_parser.get_random_comic()
    print xkcd_parser.title
    print xkcd_parser.caption
