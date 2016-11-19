#!/usr/bin/env python

import urllib2;
from bs4 import BeautifulSoup
import re
import csv
import gzip
import StringIO

hdc_url = 'https://hdchina.club/torrents.php'

f = open('hdc.cookie','r')
hdc_cookie = f.read().strip('\n') #get cookie from file and remove the enter 
f.close()

hdc_header = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.100 Safari/537.36',
    'Cookie' : hdc_cookie,
    'Accept-Encoding' : 'gzip'
}
hdc_req = urllib2.Request(hdc_url,headers=hdc_header)
hdc_pages = urllib2.urlopen(hdc_req)
#print(hdc_pages.info().get('Content-Encoding'))

if hdc_pages.info().get('Content-Encoding') == 'gzip':
    #print hdc_pages.read()
    buf = StringIO.StringIO(hdc_pages.read())
    f = gzip.GzipFile(fileobj=buf)
    hdc_html = f.read()
else:
    hdc_html = hdc_pages.read()
#print hdc_html

hdc_soup =  BeautifulSoup(hdc_html, "lxml")
hdc_fulltable = hdc_soup.find("table",{"class" : "torrent_list"})

hdc_torrents = []
for row in hdc_fulltable.find_all("tr",class_=["stickz_bg","sticky_bg"],recursive=False):
    torrent_fix = row.find("td",{"class":"t_name"}).find("tr").find_all("td")[1]
    torrent_misc = torrent_fix.h3.a
    title = torrent_misc['title']
    id = re.search(r'\d+(?=&)',torrent_misc['href']).group()
    try:
        name = torrent_fix.h4.text
    except:
        name = ''
    size = row.find("td",{"class":"t_size"}).text
    torrent = ['HDC',title,name,id,size]
    hdc_torrents.extend([torrent])


print hdc_torrents

