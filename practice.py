import urllib2
import re
import urlparse

import lxml.html


def link_crawler(seed_url, link_regex, callback=None):
    crawl_queue = [seed_url]
    seen = set(crawl_queue)
    while crawl_queue:
        url = crawl_queue.pop()
        html = download(url)
        # pass callback
        links = []
        if scrape_callback:
            links.extend(scrape_callback(url,html) or [])
        # filter links with regex
        for link in get_links(html):
            if re.match(link_regex, link):
                # form absolute link
                link = urlparse.urljoin(seed_url, link)
                # check if have already seen this link
                if link not in seen:
                    seen.add(link)
                    crawl_queue.append(link)

def download(url):
    print("Downloading: "), url
    try:
        html = urllib2.urlopen(url).read()
    except urllib2.URLError as e:
        print("Download error: "), e.reason
        html = None
        pass
    return html

def get_links(html):
    webpage_regex = re.compile('<a[^>]+href=["\'](.*?)["\']',
        re.IGNORECASE)
    all_links = webpage_regex.findall(html)
    print all_links
    return all_links
    

def scrape_callback(url, html):
    if re.search('/day/[0-9]{1,6}$', url):
        tree = lxml.html.fromstring(html)
        title = tree.cssselect('div.day-title > h1')[0].text_content().strip()
        author = tree.cssselect('span.caption')[0].text_content().strip()
        print title, author


link_crawler('http://livday.com/browse', '/day/[0-9]{1,6}$')
