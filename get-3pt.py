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

def GetMT():
    s = requests.Session()
    s.hesders.update({'Cookie':mt_cookie})
    r = requests.get(mt_url,headers=headers)
    soup =  BeautifulSoup(r.content, "lxml")
    fulltable = mt_soup.find("table",{"class" : "torrents"})
    for row in mt_fulltable.find_all("tr",class_=['sticky_top','sticky_normal'],recursive=False):
    	torrent_other = row.find_all("td",{"class":"rowfollow"})
    	size = torrent_other[3].text
    	torrent_table = row.find("table",{"class":"torrentname"})
    	torrent_img = torrent_table.find("td",{"class":"torrentimg"}).a.find("img")['src']
    	torrent_fix = torrent_table.find("td",{"class":"embedded"})
    	title = torrent_fix.a['title']
    	try:
    	    name = torrent_fix.find('br').nextSibling
    	except:
    	    name = ''
    	id = re.search(r'\d+(?=&)', torrent_fix.a['href'] ).group()

    	per_torrent = ['MT',title,name,id,size]
    	mt_torrents.extend([per_torrent])





html1 = r1.content

#r2 = urllib2.Request(url,headers=headers)
#html2 = html = urllib2.urlopen(r2).read()
