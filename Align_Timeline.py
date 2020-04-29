# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import numpy as np
from numpy import nan  

#读取Excel表格
xls_file=pd.ExcelFile('C:/Users/54365/Desktop/ag.xlsx')
xls_file.sheet_names
AG_1806=xls_file.parse('AG1806'); AG_1812=xls_file.parse('AG1812') 


#将DataFrame转为List，方便进行插入
AG_1806=np.array(AG_1806).tolist(); 
AG_1812=np.array(AG_1812).tolist()

AG_1806_new=[]; 
AG_1812_new=[];

def Merge(A,B): 
    #A,B表示要两张表格，A_append，B_append表示需要返回的值
    i=0;j=0
    A_append=[];B_append=[]; #将输入的辅助数组清空
    len_A=len(A);len_B=len(B);
    while(i<len_A and j<len_B):   
        if(A[i][0]==B[j][0]): #时间相等
            A_append.append(A[i]); B_append.append(B[j])
            i=i+1;j=j+1;
    
        elif(A[i][0]<B[j][0]):
            B_append.append([A[i][0],nan,nan]); A_append.append(A[i])
            i=i+1
        else:
            A_append.append([B[j][0],nan,nan]); B_append.append(B[j])
            j=j+1
    

    while(i<len_A):
        B_append.append([A[i][0],nan,nan,nan,nan]); A_append.append(A[i])
        i=i+1

    while(j<len_B):
        A_append.append([B[j][0],nan,nan,nan,nan]); B_append.append(B[j])
        j=j+1
    
    return A_append,B_append

AG_1806_new,AG_1812_new=Merge(AG_1806,AG_1812)

AG_1806_new=pd.DataFrame(AG_1806_new,columns=['时间','卖1价','买1价','卖一量','买一量']) 
AG_1812_new=pd.DataFrame(AG_1812_new,columns=['时间','卖1价','买1价','卖一量','卖一量']) 

AG_1806_new=AG_1806_new.fillna(method='pad')
AG_1812_new=AG_1812_new.fillna(method='pad')

AG_1806_new.to_csv('AG1806.csv')
AG_1812_new.to_csv('AG1812.csv')

a=[]
a=AG_1806_new['时间'].tolist()
b=AG_1812_new['时间'].tolist()
for (time1,time2) in zip(a,b):
    if time1!=time2:
        print("erro")
    else:
        pass
