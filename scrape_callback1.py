# -*- coding: utf-8 -*-

import re
import urlparse
import lxml.html
from crawler_ch1 import link_crawler


def scrape_callback(url, html):
    if re.search('/day/[0-9]{1,6}$', url):
        tree = lxml.html.fromstring(html)
        title = tree.cssselect('div.day-title > h1')[0].text_content().strip()
        author = tree.cssselect('span.caption')[0].text_content().strip()
        print title, author


if __name__ == '__main__':
    link_crawler('http://livday.com/browse', '/day/[0-9]{1,6}$', scrape_callback=scrape_callback)
