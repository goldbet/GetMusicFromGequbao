#-*- coding: UTF-8 -*- 
import requests
import json
import time
import webbrowser
from bs4 import BeautifulSoup

mainhttp = 'https://www.gequbao.com'
address = r"C:\Users\evative7\Desktop\Download\NewEnd"
musicList = r"C:\Users\evative7\Desktop\Download\music.txt"

def SearchMusic(_name):
    _getHtml = requests.get(mainhttp + '/s/' + _name).content.decode()
    _soup = BeautifulSoup(_getHtml, 'html.parser')
    for _soup_a in _soup.find_all('a'):
        _link = _soup_a['href']
        _text = _soup_a.get_text()
        if _text.find('翻自') != -1 | _text.find('cover') != -1:
            continue
        if _link.find('music') == -1:
            continue
        
        _songInfoHtml = requests.get(mainhttp + _link).content.decode()
        _downloadLinkStartSub = _songInfoHtml.index('const url = ')
        _downloadLinkEndSub = _songInfoHtml.index('.replace',_downloadLinkStartSub)
        _downloadLink = _songInfoHtml[_downloadLinkStartSub + "const url = ".__len__() + 1:_downloadLinkEndSub - 1].replace('&amp;','&')
        
        if _downloadLink.find('music.163') != -1:
            continue
        
        return _downloadLink
    return ""

def DownloadMusic(_musicName,_link,_address):
    try:
        _file = requests.get(_link)
        open(_address,'wb').write(_file.content)
        print(_musicName + "下载完成")
    except:
        print(_musicName + "下载错误")

fileHandler  = open(musicList,"r",encoding='utf-8')
listOfLines  =  fileHandler.readlines()
fileHandler.close()

for music in listOfLines:
    musicName = music.split('.')[1].replace('\n','')
    link = SearchMusic(musicName)
    DownloadMusic(musicName,link,address + '\\' + musicName + '.mp3')
    
