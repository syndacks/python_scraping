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
        links = []
        if callback:
            links.extend(callback(url, html) or [])
        for link in get_links(url):
            if re.match(link_regex, link):
                link = urlparse.urljoin(seed_url, link)
                if link not in seen:
                    seen.add(link)
                    crawl_queue.append(link)

def download(url):
    print 'Downloading: ', url
    try:
        html = urllib2.urlopen(url).read()
    except urllib2.URLError as e:
        print ('Download error: ', e.reason)
        html = None
        pass
    print html
    return html


def get_links(url):
    webpage_regex = re.compile('<a[^>]+href=["\'](.*?)["\']',
        re.IGNORECASE)
    regex_links = webpage_regex.findall(url)
    return regex_links


def callback(url, html):
    if re.search('/day/[0-9]{1,6}$'):
        tree = lxml.html.fromstring(html)
        title = tree.cssselect()[0].text_content().strip()
        print title, author
    return
