# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import pandas as pd

df=pd.read_csv('a.txt',sep='|',names=['time','imse'])

grouped=df.groupby(['time']).size()

time_list=list(grouped.index)  #获取时间列表

for i in time_list:  
    df1=df.groupby(df.time==i)  #根据时间进行聚合，返回一个groupby方法
    file_name=str(i)+".txt"  #设置文件名，为"日期+.txt"的格式
    df3=df1.get_group(True)#将分组结果，结果为True即含有的保存为df3
    df3.to_csv(file_name,sep='|',index=False,header=False)
