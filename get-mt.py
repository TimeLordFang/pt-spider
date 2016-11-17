#!/usr/bin/env python

import urllib2;
from bs4 import BeautifulSoup
import re
import csv
import gzip
#from StringIO import StringIO
import StringIO


mt_url = 'https://tp.m-team.cc/torrents.php'

f = open('mt.cookie','r')
mt_cookie = f.read().strip('\n') #get cookie from file and remove the enter 
f.close()

mt_header = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.100 Safari/537.36',
    'Cookie' : mt_cookie,
    'Accept-Encoding' : 'gzip'
}
mt_req = urllib2.Request(mt_url,headers=mt_header)
mt_pages = urllib2.urlopen(mt_req)
#print(mt_pages.info().get('Content-Encoding'))

if mt_pages.info().get('Content-Encoding') == 'gzip':
    #print mt_pages.read()
    buf = StringIO.StringIO(mt_pages.read())
    f = gzip.GzipFile(fileobj=buf)
    mt_html = f.read()
else:
    mt_html = mt_pages.read()
#print mt_html

mt_soup =  BeautifulSoup(mt_html, "lxml")
mt_fulltable = mt_soup.find("table",{"class" : "torrents"})
td_th = re.compile('t[dh]')

mt_torrents = []
for row in mt_fulltable.find_all("tr",class_=['sticky_top','sticky_normal'],recursive=False):
    torrent_other = row.find_all("td",{"class":"rowfollow"})
    size = torrent_other[3].text
    torrent_table = row.find("table",{"class":"torrentname"})
    torrent_img = torrent_table.find("td",{"class":"torrentimg"}).a.find("img")['src']
    torrent_fix = torrent_table.find("td",{"class":"embedded"})
    torrent_title = torrent_fix.a['title']
    torrent_name = torrent_fix.find('br').nextSibling
    torrent_id = re.search(r'\d+(?=&)', torrent_fix.a['href'] ).group()

    per_torrent = [torrent_title,torrent_name,torrent_img,torrent_id,size]
    #print per_torrent
    mt_torrents.extend([per_torrent])

    #print torrent_title
    #print torrent_name
    #print torrent_img
    #print torrent_id
    #print size
print mt_torrents


