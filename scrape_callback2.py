# -*- coding: utf-8 -*-

import csv
import re
import urlparse
import lxml.html
from crawler_ch1 import link_crawler


class ScrapeCallback:
    def __init__(self):
        self.writer = csv.writer(open('days.csv', 'w'))
        self.fields = ('title', 'author')
        self.writer.writerow(self.fields)

    def __call__(self, url, html):
        if re.search('/day/[0-9]{1,6}$', url):
            tree = lxml.html.fromstring(html)
            row = []
            title = tree.cssselect('div.day-title > h1')[0].text_content().strip()
            author = tree.cssselect('span.caption')[0].text_content().strip()
            row.append(title)
            row.append(author)
            self.writer.writerow(row)
        #
        # if re.search('/view/', url):
        #     tree = lxml.html.fromstring(html)
        #     row = []
        #     for field in self.fields:
        #         row.append(tree.cssselect('table > tr#places_{}__row > td.w2p_fw'.format(field))[0].text_content())
        #     self.writer.writerow(row)


if __name__ == '__main__':
    link_crawler('http://livday.com/browse', '/day/[0-9]{1,6}$', scrape_callback=ScrapeCallback())
