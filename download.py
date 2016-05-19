# -*- coding: utf-8 -*-

import urllib2
import urllib
import re
import thread
import time,string


class Spider_Model:

    def __init__(self,list):
        self.pages = []
        self.enable = False
        self.list =list
        self.count=1

    # 将所有的段子都扣出来，添加到列表中并且返回列表
    def GetPage(self,list):
        myUrl = 'http://www.caship.ac.cn/search/detail/?guobie=%E4%B8%AD%E5%9B%BD%E4%B8%93%E5%88%A9&id='+str(list)
        print myUrl
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        headers = { 'User-Agent' : user_agent }
        req = urllib2.Request(myUrl, headers = headers)
        try:myResponse = urllib2.urlopen(req)
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
        print myItems
        #myItems = re.findall('<div.*?class="content">(.*?)</div>',unicodePage,re.S)
        return myItems

    # 用于加载新的段子
    def LoadPage(self):
        # 如果用户未输入quit则一直运行
        while self.enable:
            # 如果pages数组中的内容小于2个
            if len(self.pages) < 2:
                    # 获取新的页面中的段子们
                   # time.sleep(5)
                  if self.list:
                       try:
                          myPage = self.GetPage(self.list[0])
                          self.pages.append(myPage)
                          del (self.list[0])
                       except:
                          print "error"
                  else:
                      return

            else:
                time.sleep(1)

    def ShowPage(self,nowPage):
        for items in nowPage:
            f=file("address.txt","a+")
            f.write(items+'\n')
            f.close()
            sName = string.zfill(self.count,5) + '.pdf'#自动填充成六位的文件名
            self.count+=1
            url="http://www.caship.ac.cn/search/fulltext"+items
            urllib.urlretrieve(url, sName)
            print u'打印'  , items


    def Start(self):
        self.enable = True

        print u'正在加载中请稍候......'

        # 新建一个线程在后台加载段子并存储
        thread.start_new_thread(self.LoadPage,())

        #----------- 加载处理糗事百科 -----------
        while self.enable:

            # 如果self的page数组中存有元素
            if len(self.pages)>0:
                print "size of pages"+str(len(self.pages))
                nowPage = self.pages[0]
                del self.pages[0]
                self.ShowPage(nowPage)
            else:
                if len(self.list) == 0:
                    return


def readline(file):
    f = open(file)             # 返回一个文件对象
    list=[]
    line = f.readline()             # 调用文件的 readline()方法
    list.append(line)
    while line:
       print line,                 # 后面跟 ',' 将忽略换行符
    # print(line, end = '')　　　# 在 Python 3中使用
       line = f.readline()
       list.append(line)
    return list






print u'请按下回车浏览今日的糗百内容：'
raw_input(' ')
list=readline("hello.txt")
myModel = Spider_Model(list)
myModel.Start()