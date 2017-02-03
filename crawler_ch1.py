import urllib2
import re
import itertools
import urlparse


def link_crawler(seed_url, link_regex, scrape_callback=None):
    '''Crawl from the given seed URL following links matched by regex
    '''
    # the original url that will start it al off
    crawl_queue = [seed_url]
    # keep track which URL's have seen before
    seen = set(crawl_queue)
    while crawl_queue:
        url = crawl_queue.pop()
        html = download(url)
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

def download(url, user_agent='wswp', num_retries=2):
    print 'Downloading:', url
    headers = {'User-agent': user_agent}
    request = urllib2.Request(url, headers=headers)
    try:
        html = urllib2.urlopen(request).read()
    except urllib2.URLError as e:
        print 'Download error:', e.reason
        html = None
        if num_retries > 0:
            if hasattr(e, 'code') and 550 <= e.code < 600:
                # recursively retry 5xx HTTP errors
                return download(url, num_retries-1)
    return html


def get_links(html):
    '''return a list of links from html
    '''
    # a regex to extract all links from the webpage
    webpage_regex = re.compile('<a[^>]+href=["\'](.*?)["\']',
        re.IGNORECASE)
    # list of all links from the webpage
    return webpage_regex.findall(html)




## IF A SITE HAS A SITEMAP (UNLIKELY)
# def crawl_sitemap(url):
#     # download the sitemap file
#     sitemap = download(url)
#     # extract the sitemap links
#     links = re.findall('<loc>(.*?)</loc>', sitemap)
#     # download each link
#     for link in links:
#         html = download(link)
#         # scrape html here
#         # ...

## IF A SITE HAS A SEQUENTIAL ROUTING SYSTEM (NOT VERY LIKELY)
# for page in itertools.count(220):
#     max_errors = 5
#     num_errors = 0
#     url = 'http://livday.com/day/000%d' % page
#     html = download(url)
#     if html is None:
#         num_errors += 1
#         if num_errors == max_errors:
#             break
#     else:
#         # success - can scrape the result
#         pass
