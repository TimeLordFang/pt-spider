#!/usr/bin/env python

import urllib2;
from bs4 import BeautifulSoup
import re
import csv
import gzip
import StringIO

ttg_url = 'https://totheglory.im/browse.php?c=M'

f = open('ttg.cookie','r')
ttg_cookie = f.read().strip('\n') #get cookie from file and remove the enter 
f.close()

ttg_header = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.100 Safari/537.36',
    'Cookie' : ttg_cookie,
    'Accept-Encoding' : 'gzip'
}
ttg_req = urllib2.Request(ttg_url,headers=ttg_header)
ttg_pages = urllib2.urlopen(ttg_req)
#print(ttg_pages.info().get('Content-Encoding'))

if ttg_pages.info().get('Content-Encoding') == 'gzip':
    buf = StringIO.StringIO(ttg_pages.read())
    f = gzip.GzipFile(fileobj=buf)
    ttg_html = f.read()
else:
    ttg_html = ttg_pages.read()
#print ttg_html

ttg_soup =  BeautifulSoup(ttg_html, "lxml")
ttg_fulltable = ttg_soup.find("table",{"id" : "torrent_table"})

ttg_torrents = []
for row in ttg_fulltable.find_all("tr",class_=["hover_hr  sticky","hover_hr"],recursive=False):
    id = row["id"]
    size = row.find_all("td",{"align":"center"})[3].text
    torrent_fix = str(row.find("td",{"align":"left"}).find("div").a.b).split('<br/>')   #.find("br").next_sibling
    title = re.sub(r'</?\w+[^>]*>','',torrent_fix[0])
    try:
        name = re.sub(r'</?\w+[^>]*>','',torrent_fix[1]).strip()
    except:
        name = ''

    torrent = ['TTG',title,name,id,size]
    ttg_torrents.extend([torrent])



print ttg_torrents

