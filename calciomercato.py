#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib.request 
from bs4 import BeautifulSoup
import html, time
import pathlib

dir_path = str(pathlib.Path.cwd()) + '/'

def filterLatest(art_list):
    jugadores = open(dir_path + 'jugadores.txt').readlines()
    jugadores = [' '.join(j.strip().split(' ')[1:]) for j in jugadores]
    equipos = open(dir_path + 'equipos.txt').readlines()
    equipos = [j.strip() for j in equipos]
    whitelist = list(set(jugadores+equipos))
    print(whitelist)
    retVal = []
    for art in art_list:
        good = False
        for e in whitelist:
            if e in art['title'] or e in art['body']:
                good = True
                break
        if good:
            retVal.append( art )
        else:
            print('INFO: filtering out (no whitelist keywords) -> ' + art['item'])
    return retVal


def getLatest(url='https://www.calciomercato.com/feed/mercato', debug=False):
#def getLatest(url='https://www.calciomercato.com/feed', debug=False):
    retVal = []

    if debug:
        response_text = open(dir_path + 'feed.xml').read()
    else:
        response = urllib.request.urlopen( url ) 
        response_text = response.read() 
        #open('feed.xml', 'w').write( str(response_text, 'utf-8') )

    soup = BeautifulSoup(response_text, 'html.parser')

    for i in soup.find_all('item')[:10]:
        out_item = {}
        item = BeautifulSoup(str(i), 'html.parser')
        item_url = 'https://www.calciomercato.com/news/' + html.unescape(item.guid.text)
        print(html.unescape(item.title.text))
        pubDate = html.unescape(item.pubdate.text).replace(',','').replace(' ','_')
        print (pubDate)
        out_item['title'] = html.unescape(item.title.text)
        if out_item['title'].startswith("'"):
            out_item['title'] = out_item['title'][1:]
        if out_item['title'].endswith("'"):
            out_item['title'] = out_item['title'][:-1]
        print(item_url)
        out_item['item_url'] = item_url
        out_item['item'] = pubDate + '_' + html.unescape(item.guid.text)
        print(out_item['item'])
        response = urllib.request.urlopen( item_url ) 
        item_text = response.read() 
        soup = BeautifulSoup(item_text, 'html.parser')
        # <div class="article-body">
        bodies = soup.find_all(attrs={"class": "text", "id":"article-body"})
        if len(bodies) == 1:
            body = bodies[0].text.replace('Commenta per primo','').strip()
            try:
                someint = int(body.split('\n')[0])
                body = '\n'.join( body.split('\n')[1:] ).strip()
            except:
                continue
            if body[0] in ['1','2','3','4','5','6','7','8','9']:
                body = body[1:].strip()
            if body.splitlines()[-1].startswith('.find'):
                body = '\n'.join(body.splitlines()[:-1]).strip()
            #print(body)
            out_item['body'] = body
        # <meta name="twitter:image:src" content="https://cdn.calciomercato.com/images/2019-01/zurkowski.fiorentina.2018.19.visite.750x450.jpg"/>
        photos = soup.find_all(attrs={"name": "twitter:image:src"})
        if len(photos) == 1:
            print(photos[0]['content'])
            out_item['image'] = photos[0]['content']
            # https://freeimage.host/page/api
        retVal.append( out_item )
        time.sleep(10.0)
        print('INFO: sleeping 10 seconds after requesting an article to new site ...')
            
        print('-'*80)
    return retVal

if __name__ == '__main__':
    print(getLatest())
    
    





