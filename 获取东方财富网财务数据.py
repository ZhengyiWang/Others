from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time
import pandas as pd
import os
from time import sleep

#模拟页面
chrome_options = webdriver.ChromeOptions()
browser = webdriver.Chrome(chrome_options=chrome_options) #打开网页
browser.minimize_window()  # 最小化窗口
wait = WebDriverWait(browser, 10) #设置等待避免由于网络延迟或浏览器卡顿导致的偶然失败

#创建dataframe
df=pd.DataFrame()

start_year=int(input('请输入查询起始年份:'))
end_year =int(input('请输入查询结束年份:'))

report_type=input('请输入报表类型:业绩报表，资产负债表，利润表，现金流量表：')
if report_type=='业绩报表':
    report_type='yjbb'
elif report_type=='资产负债表':
    report_type='zcfz'
elif report_type=='利润表':
    report_type='lrb'
elif report_type=='现金流量表':
    report_type='xjll'


#获取2021年数据
for p in range(start_year,end_year+1):
    url = 'http://data.eastmoney.com/bbsj/'+str(p)+'12/'+report_type+'.html' #获取当年业绩报表网址
    print(url)   
    browser.get(url)  #获取当前网页
    i=1
    page=0
    while True:
        element = browser.find_elements_by_class_name("dataview-body") #获取表格主体
        tb = pd.read_html(element[0].get_attribute("outerHTML"))[0] #利用read_html函数获取表格内容
        tb["年份"]=p #添加年份属性
        df=df.append(tb)
        
        #判断是否最后一页
        nextpage = browser.find_elements_by_link_text("下一页")
        if len(nextpage)==0:
            break

        i=i+1
        
        #模拟翻页功能
        while True:
            try:
                next_page =wait.until(EC.presence_of_element_located((By.LINK_TEXT,"下一页")))
                wait.until(EC.element_to_be_clickable((By.LINK_TEXT,"下一页"))  )
                next_page.click()
                if wait.until(EC.text_to_be_present_in_element((By.CLASS_NAME,"active"), str(i))):
                    break
            except:
                pass
    
    #避免翻页过于频繁被ban
    sleep(1)  

file_name=str(start_year)+'_'+str(end_year)+str(report_type)+'.xlsx'

df.to_excel(file_name)

#在excel表上直接删除第一行，修改schema
df_zcfz=pd.read_excel('2021_2022zcfz.xlsx')
df_lrb=pd.read_excel('2021_2022lrb.xlsx')
result=pd.merge(df_lrb,df_zcfz,on='股票代码')


#将万和亿改成整数
def str_to_num(x):
    if x[-1]=='亿':
        x=float(x[:-1])*10000000
    elif x[-1]=='万':
        x=float(x[:-1])*10000
    return x

result['净利润(元)']=result['净利润(元)'].apply(lambda x:str_to_num(x))
result['总资产(元)']=result['总资产(元)'].apply(lambda x:str_to_num(x))
result['ROA']=result['净利润(元)']/result['总资产(元)']
result=result.set_index(['股票代码'])
