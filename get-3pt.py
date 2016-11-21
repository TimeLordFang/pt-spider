#!/usr/bin/env python 

import requests
import urllib2

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.100 Safari/537.36',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4',
    'Accept-Encoding': 'gzip, deflate,'
    }

f = open('pts.cookie','r')
mt_cookie = f.readline()[0].strip()
ttg_cookie = f.readline()[1].strip()
hdc_cookie = f.readline()[2].strip()
f.close()

mt_url = 'https://tp.m-team.cc/torrents.php'
ttg_url = 'https://totheglory.im/browse.php?c=M'
hdc_url = 'https://hdchina.club/torrents.php'
r1 = requests.get(url,headers=headers)
r2 = urllib2.Request(url,headers=headers)

html1 = r1.content
html2 = html = urllib2.urlopen(r2).read()

print "html1:\n"
print html1,"\n\n"
print "html2:\n"
print html2
