from datetime import datetime
import requests
from lxml import html

page = requests.get("http://learningenglish.voanews.com/a/3624829.html")
tree = html.fromstring(page.content)

title = tree.xpath('//*[@id="content"]/div[2]/div/div/div/div[1]/h1/text()')[0]
date = tree.xpath('//*[@id="content"]/div[2]/div/div/div/div[2]/div/div/span/time/text()')[0]
videoUrl = tree.xpath('//*[@id="content"]/div[2]/div/div/div/div[4]/div/div[1]/video/@src')[0]
description = tree.xpath('//*[@id="content"]/div[3]/div/div[1]/div/p/text()')[0]

metadata = {
'title': title,
'date': date,
'videoUrl': videoUrl,
'description': description
}

print metadata
