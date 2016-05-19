# -*- coding: utf-8 -*-

import urllib2
import urllib
import re
import thread
import time,string
import sys


#----------- 加载处理糗事百科 -----------
class Spider_Model:

    def __init__(self,content):
        self.content=content
        self.count=0  #number of pdf downloaded
        self.page = 1 #the searching page are visiting
        self.pagenumber=0# numeber of the searching page
        self.pages = []
        self.enable = False


    def GetPage(self,page):
        myUrl = "http://www.caship.ac.cn/search/search/?guobie=%E4%B8%AD%E5%9B%BD%E4%B8%93%E5%88%A9&w=query&wd="+self.content+"&s1=%E6%90%9C+%E7%B4%A2&listtype=&page="+str(page)
       # print myUrl
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        headers = { 'User-Agent' : user_agent }
        req = urllib2.Request(myUrl, headers = headers)
        myResponse = urllib2.urlopen(req)
        myPage = myResponse.read()#encode的作用是将unicode编码转换成其他编码的字符串，decode的作用是将其他编码的字符串转换成unicode编码
        unicodePage = myPage.decode("utf-8")

        #re.S是任意匹配模式，也就是.可以匹配换行符
       # myItems = re.findall('(/Home/DownloadChoice/\d+)',unicodePage,re.S)
        myItems = re.findall('&id=(\d+).*? <span style="font-size:12px;">(.*?)</span>',unicodePage,re.S)
        #myItems = re.findall('<div.*?class="content">(.*?)</div>',unicodePage,re.S)
        return myItems


    def LoadPage(self):
        # 如果用户未输入quit则一直运行
        while self.enable:
            # 如果pages数组中的内容小于2个
            if len(self.pages) < 2:
                   # time.sleep(5)
                    myPage = self.GetPage(self.page)
                    self.page += 1
                    self.pages.append(myPage)
                    if self.page>self.pagenumber:
                        return
            else:
                time.sleep(1)

    def ShowPage(self,nowPage):
        for items in nowPage:
           if items[1][6] == '1':
            self.SavePage(items[0])
            print u'发明专利'  , items[1]
           else:
            print u'其他专利'  , items[1]

    def SavePage(self,nowPage):
       list=self.Getdownload(nowPage)
       for item in list:
        print item
        reObj1 = re.compile('/(CN(\.|\w)*pdf)')
        result=reObj1.findall(item)
        if len(result)!=0:
         print "retult="
         print result
         sName = result[0][0]
         print sName

         if sName[6]!='1':
            print "unvaliable"
            return
         url="http://www.caship.ac.cn/search/fulltext"+item
         try:
            req=urllib2.Request(url)
            myResponse = urllib2.urlopen(req)
            print url
            if int(myResponse.info().getheader('Content-Length'))< 10240:
                print myResponse.info().getheader('Content-Length')+"  too small"
                return
            urllib.urlretrieve(url, sName)
            self.count+=1
         except urllib2.URLError, e:
                 print e.reason


    def Getdownload(self,list):
        myUrl = 'http://www.caship.ac.cn/search/detail/?guobie=%E4%B8%AD%E5%9B%BD%E4%B8%93%E5%88%A9&id='+str(list)
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        headers = { 'User-Agent' : user_agent }
        req = urllib2.Request(myUrl, headers = headers)
        try: myResponse = urllib2.urlopen(req)
        except urllib2.URLError, e:
          print e.reason
        myPage = myResponse.read()
        #encode的作用是将unicode编码转换成其他编码的字符串
        #decode的作用是将其他编码的字符串转换成unicode编码
        unicodePage = myPage.decode("utf-8")

        # 找出所有class="content"的div标记
        #re.S是任意匹配模式，也就是.可以匹配换行符
       # myItems = re.findall('(/Home/DownloadChoice/\d+)',unicodePage,re.S)
        myItems = re.findall('fulltext(.*\.pdf)',unicodePage,re.S)
        #print myItems
        #myItems = re.findall('<div.*?class="content">(.*?)</div>',unicodePage,re.S)
        return myItems

    def Getpagenumber(self):
        myUrl = "http://www.caship.ac.cn/search/search/?guobie=%E4%B8%AD%E5%9B%BD%E4%B8%93%E5%88%A9&w=query&wd="+self.content+"&s1=%E6%90%9C+%E7%B4%A2&listtype=&page=1"
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        headers = { 'User-Agent' : user_agent }
        req = urllib2.Request(myUrl, headers = headers)
        myResponse = urllib2.urlopen(req)
        myPage = myResponse.read()
        unicodePage = myPage.decode("utf-8")
        print unicodePage
        myItems = re.findall('(\d+)</a>&nbsp;\s+</li>',unicodePage,re.S)
        return myItems[0]

    def down(self):
         while self.enable:
            # 如果self的page数组中存有元素
            if self.pages:
                nowPage = self.pages[0]
                del self.pages[0]
                self.ShowPage(nowPage)
            else:
                if self.page>self.pagenumber:
                    return

    def Start(self):
        self.enable = True
        self.pagenumber=self.Getpagenumber()
        page = self.page
        print u'正在加载中请稍候......'
        thread.start_new_thread(self.LoadPage,())
        thread.start_new_thread(self.down,())
        thread.start_new_thread(self.down,())
        thread.start_new_thread(self.down,())
        thread.start_new_thread(self.down,())
        thread.start_new_thread(self.down,())





def getResourceLength(url):
       req=urllib2.Request(url)
       response = urllib2.urlopen(req)
       print  'size'+response.info().getheader('Content-Length')
       return

print 'press enter to start：'
raw_input(' ')
while(1):
 content=raw_input("input what to search")
 print content
 myModel = Spider_Model(content)
 print myModel.Getpagenumber()
 myModel.Start()
sys.exit(0)