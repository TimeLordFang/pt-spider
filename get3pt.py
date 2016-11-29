#!/usr/bin/env python 

from bs4 import BeautifulSoup
import re
import requests
#import urllib2
import threading
import sqlite3


headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.100 Safari/537.36',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4',
    'Accept-Encoding': 'gzip, deflate,'
    }

#f = open('pts.cookie','r')
#mt_cookie = f.readline()[0].strip()
#ttg_cookie = f.readline()[1].strip()
#hdc_cookie = f.readline()[2].strip()
#f.close()
mt_url = 'https://tp.m-team.cc/torrents.php'
ttg_url = 'https://totheglory.im/browse.php?c=M'
hdc_url = 'https://hdchina.club/torrents.php'

#db_conn = sqlite3.connect('torrs.db')
#db_conn.execute('''
#    CREATE TABLE TORRS
#    (ID INTEGER PRIMARY KEY  AUTOINCREMENT,
#    SITE    TEXT NOT NULL,
#    TITLE   TEXT NOT NUll,
#    NAME    TEXT NOT NULL,
#    T_ID    INT NOT NULL,
#    SIZE    TEXT NOT NULL
#    )''')
#mt_torrents = []
#hdc_torrents = []
#ttg_torrents = []
def GetMT():
    f = open('mt.cookie','r')
    mt_cookie = f.read().strip()
    f.close()
    s = requests.Session()
    s.headers.update({'Cookie':mt_cookie})
    r = s.get(mt_url,headers=headers)
    soup =  BeautifulSoup(r.content, "lxml")
    fulltable = soup.find("table",{"class" : "torrents"})
    mt_torrents = []
    for row in fulltable.find_all("tr",class_=['sticky_top','sticky_normal'],recursive=False):
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

        mt_torrents.append("MT--"+name+"--"+size)
    	#per_torrent = ['MT',title,name,id,size]
    	#mt_torrents.extend([per_torrent])
    return mt_torrents

def GetTTG():
    f = open('ttg.cookie','r')
    ttg_cookie = f.read().strip()
    f.close()
    s = requests.Session()
    s.headers.update({'Cookie':ttg_cookie})
    r = s.get(ttg_url,headers=headers)
    soup =  BeautifulSoup(r.content, "lxml")
    fulltable =  soup.find("table",{"id" : "torrent_table"})
    ttg_torrents = []
    for row in fulltable.find_all("tr",class_=["hover_hr  sticky","hover_hr"],recursive=False):
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
    return ttg_torrents

def GetHDC():
    f = open('hdc.cookie','r')
    hdc_cookie = f.read().strip()
    f.close()
    s = requests.Session()
    s.headers.update({'Cookie':hdc_cookie})
    r = s.get(hdc_url,headers=headers)
    soup =  BeautifulSoup(r.content, "lxml")
    fulltable = soup.find("table",{"class" : "torrent_list"})
    hdc_torrents = []
    for row in fulltable.find_all("tr",class_=["stickz_bg","sticky_bg"],recursive=False):
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
    return hdc_torrents


threads = []
t1 = threading.Thread(target=GetMT)
threads.append(t1)
t2 = threading.Thread(target=GetHDC)
threads.append(t2)
t3 = threading.Thread(target=GetTTG)
threads.append(t3)
if __name__ == '__main__':
    for t in threads:
        t.setDaemon(True)
        t.start()
    all_torrents = GetMT() + GetHDC() + GetTTG()
    #all_torrents = ttg_torrents + hdc_torrents + mt_torrents
    #print all_torrents.encode('utf-8')
    for i in all_torrents:
        print i[1]
        print i[2]
