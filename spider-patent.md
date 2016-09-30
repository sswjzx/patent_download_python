---
title: spider-patent
date: 2016-10-01 02:58:59
tags:
---
# 专利爬虫－中科院知识产权

标签（空格分隔）： 爬虫

---

本科毕设是关于专利分析，因为需要语料库，所以只能编写爬虫程序下载专利文件进行分析．参考博文：[糗事百科爬虫分析](http://blog.csdn.net/pleasecallmewhy/article/details/8932310)

---
# 爬虫程序构成

## 使用说明　Ｕｓａｇｅ

    输入要下载专利的关键字：ｘｘ
    将所有相关专利下载于文件夹：ｘｘ_result

## 变量声明

```python
        self.content=content #下载专利的关键字
        self.count=0  #number of pdf downloaded/已经下载好专利的数目
        self.page = 1 #the searching page are visiting/正在访问的页码数
        self.pagenumber=0# numeber of the searching page/总共的页码数
        self.pages = []　# 得到的存放着还没有下载的专利详情页url
        self.enable = False #当为ｔｒｕｅ，表示下载结束
```

## 模块说明

+  def GetPage(self,page)

    page为搜索结果的页码数，获取指定页码数的搜索结果网页
    并返回html网页中所专利的详情页url的list

+  def LoadPage(self):

    加载搜索结果页面，直至遍历了所有搜索结果的页码

+  def ShowPage(self,nowPage):

    打印专利编号，并按照编号规则将专利分为　__发明专利__　和　__其他专利__
    只下载发明专利

+  def SavePage(self,nowPage):

    获得专利标识符后，构造专利下载url，并叫下载超时或者下载文件过小的错包丢弃．


+  def Getdownload(self,list):

    从专利详情页中获取专利的下载url的标识符

> 如:[u'/sipo_doc_01/201504/CN201410259207.0/combine/CN201410259207.0.pdf']
　　

+  def Getpagenumber(self):

    返回搜索页面的总页码数

+  def down(self):

    从self.pages中获取专利详情页，并下载专利，当同时满足以下两个条件时返回：

    - 已经遍历了所有搜索页面

    - pages为空

+  def Start(self):

    １个线程获取专利下载地址    
    ５个线程下载专利



> mark:os.mkdir() permision deny http://www.cnblogs.com/mecca/p/3717891.html
> print  os.getcwd()+'/'+content.decode('utf-8')+'_result/'+sName
urllib.urlretrieve(url, os.getcwd()+'/'+content.decode('utf-8')+'_result/'+sName)
        绝对路径与编码
