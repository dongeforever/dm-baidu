#!/usr/bin/env python
# coding=utf-8
#########################################
	#> File Name: crawler.py
	#> Author: nealgavin
	#> Mail: nealgavin@126.com 
	#> Created Time: Tue 27 May 2014 03:42:54 PM CST
#########################################

import random
import socket
import urllib2
import urllib
import re
import string
from bs4 import BeautifulSoup
import sys
import cookielib

ERROR = {
        '0':'Can not open the url,checck you net',
        '1':'Creat download dir error',
        '2':'The image links is empty',
        '3':'Download faild',
        '4':'Build soup error,the html is empty',
        '5':'Can not save the image to your disk',
    }

class BrowserBase(object): 
    def __init__(self):
        socket.setdefaulttimeout(20)
        self.HTML = ''
        self.articleName = ''
        self.link = ''
    def speak(self,name,content):
        print '[%s]%s' %(name,content)

    def openurl(self,url):
        cookie_support= urllib2.HTTPCookieProcessor(cookielib.CookieJar())
        self.opener = urllib2.build_opener(cookie_support,urllib2.HTTPHandler)
        urllib2.install_opener(self.opener)
        user_agents = [
                    'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
                    'Opera/9.25 (Windows NT 5.1; U; en)',
                    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
                    'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
                    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
                    'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
                    "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
                    "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 ",

                    ] 
       
        agent = random.choice(user_agents)
        self.opener.addheaders = [("User-agent",agent),("Accept","*/*"),('Referer','http://www.google.com')]
        try:
            res = self.opener.open(url)
            self.HTML = res.read()
#            print res.read()
        except Exception,e:
            self.speak(str(e),url)
            raise Exception
        else:
            return res
    def OUT(self):
        print self.HTML

    def getArticleName(self,tags):

        re_rules = r'<span class="(.+?)"><a href="(.+?)">(.+?)</a>'
        p = re.compile(re_rules,re.DOTALL)
        title = p.findall(str(tags))
        self.chineseListOut(title)

    def chineseListOut(self,tags):
        title = []
        for tag in tags:
            for ele in tag:
#                print '+',str(ele),'-'
                title.append(ele.strip())
        self.link = "http://blog.csdn.net" + title[1]
        tle = title[2].split()
        self.articleName = '-'.join(tle)

    def buildArticleHTML(self):
        self.HTML = str(self.HTML)
        self.HTML = '<html><meta charset="utf-8"><body>'+self.HTML
        self.HTML = self.HTML + '</body><html>'

    def getMainArticle(self):
        """get the main article of CSDN blog"""
        soup = BeautifulSoup(self.HTML)
        tags_all = soup.findAll('div',{'class':'article_title'})
        print tags_all
        self.getArticleName(tags_all)
        tags_all = soup.findAll('div',{'id':'article_content','class':'article_content'})
        self.HTML = tags_all[0]
        self.buildArticleHTML()
    
    def saveArticleAsHTML(self):
        filePath = self.articleName+'.html'
        try:
            
            filePointer = open(filePath,'w+')
        except:
            print 'open error'
        print 'path = ',filePath
        filePointer.write(self.HTML)
        filePointer.close()

browser = BrowserBase()
url = raw_input('Input the links of CSDN article you needed!\n')
if url is None or len(url) == 0:
    url = "http://blog.csdn.net/nealgavin/article/details/27110717"
browser.openurl(url)
browser.getMainArticle()
browser.saveArticleAsHTML()
