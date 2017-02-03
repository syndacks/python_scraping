import mechanize

URL = 'https://newyork.craigslist.org/search/bik'
URL2 = 'http://www.yahoo.com'

def is_there_caad10():
    # create a broser
    b = mechanize.Browser()

    # disable loading robots.text
    b.set_handle_robots(False)

    # navigate
    b.open(URL2)

    # choose a form
    b.select_form(nr=0)

    # fill it out
    b['p'] = 'pycon'

    # submit
    fd = b.submit()

is_there_caad10()
