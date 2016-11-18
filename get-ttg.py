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
    #print ttg_pages.read()
    buf = StringIO.StringIO(ttg_pages.read())
    f = gzip.GzipFile(fileobj=buf)
    ttg_html = f.read()
else:
    ttg_html = ttg_pages.read()
#print ttg_html

ttg_soup =  BeautifulSoup(ttg_html, "lxml")
ttg_fulltable = ttg_soup.find("table",{"class" : "torrent_table"})

ttg_torrents = []
for row in ttg_fulltable.find_all("tr",class_=["hover_hr  sticky","hover_hr"],recursive=False):
    id = row["id"]
    torrent_fix = row.find("td",{"class":"t_name"}).find("tr").find_all("td")[1]
    torrent_misc = torrent_fix.h3.a
    title = torrent_misc['title']
    id = re.search(r'\d+(?=&)',torrent_misc['href']).group()
    name = torrent_fix.h4.text
    size = row.find("td",{"class":"t_size"}).text
    #print title
    #print name
    #print id
    #print size
    torrent = [title,name,id,size]
    ttg_torrents.extend([torrent])


print ttg_torrents

