# -*- coding: utf-8 -*-
"""
Created on Thu May 24 19:05:23 2018

@author: 54365
"""

from urllib import request
from bs4 import BeautifulSoup
import re

#创建txt文件
file = open('警花相伴.txt', 'w', encoding='utf-8')
target_url = 'http://www.xiaoqiangxs.cc/3/3023/'
#User-Agent
head = {}
head['User-Agent'] = 'Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166  Safari/535.19'
target_req = request.Request(url = target_url, headers = head)
target_response = request.urlopen(target_req)
target_html = target_response.read().decode('gbk','ignore')
#创建BeautifulSoup对象
listmain_soup = BeautifulSoup(target_html,'lxml')
#搜索文档树,找出div标签中class为listmain的所有子标签
chapters = listmain_soup.find_all('div',class_='liebiao')
#使用查询结果再创建一个BeautifulSoup对象,对其继续进行解析
download_soup = BeautifulSoup(str(chapters), 'lxml')
#计算章节个数
#开始记录内容标志位,只要正文卷下面的链接,最新章节列表链接剔除
chapter_list = download_soup.find_all("a", attrs={"style": "", "href": re.compile(r"/.*\.html")})  
for x in chapter_list:  
    file_url = x.attrs["href"]  # 获取a标签中href属性里面的值
    download_url="http://www.xiaoqiangxs.cc/" + file_url
    
    download_req = request.Request(url = download_url, headers = head)
    download_response = request.urlopen(download_req)
    download_html = download_response.read().decode('gbk','ignore')
    soup_texts = BeautifulSoup(download_html, 'lxml')
    texts = soup_texts.find_all(id = 'content')
    soup_text = BeautifulSoup(str(texts), 'lxml')
    #将\xa0无法解码的字符删除
    file.write(soup_text.div.text.replace('\xa0',''))
file.close()