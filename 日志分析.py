# -*- coding: utf-8 -*-
"""
Created on Thu Sep 10 13:54:47 2020

@author: dell
"""

import sys
import traceback
from datahub import DataHub
from datahub.exceptions import ResourceExistException
from datahub.models import FieldType, RecordSchema, TupleRecord, BlobRecord, CursorType, RecordType
import pandas as pd
import numpy as np



def GetMiddleStr(content,startStr,endStr):
  startIndex = content.index(startStr)
  if startIndex>=0:
    startIndex += len(startStr)
  endIndex = content.index(endStr)
  return content[startIndex:endIndex]

#line='[app_zt] 2020-09-09 00:27:46 [DEBUG] (ServiceUtil:84) req={"function_id": "X300010","passkey": "Jm7coOdhcs2t4BgN1b9\/BjQoQ44Vf0O3zDCyxBxqdN7CZfY74WmN7g==","mobile": "13987654321","app_id": "XC","chanel_id": "1","op_station": "XC,101.231.45.186,cb0c0153037111e98746000c2992639d,864688038461619,xiaomi_MI 6X_28_9,6.02,TDX_GPHONE,"},res={"rs":[{"valid_end_date":20201215,"valid_begin_date":20200311,"level2_name":"湘财Level-2(沪深)","client_reg_id":199242,"first_buy_date":20200311,"mobile":"13987654321","total_buy_num":5}],"error_no":0}'
#tmp=eval(GetMiddleStr(line, 'req=', ',res='))

f = open("web.log",'rb')
lines = f.readlines()
count=0
log=[]
matcher='(ServiceUtil:84)'
for line in lines:
    if  matcher in str(line):
        count=count+1
        tmp=GetMiddleStr(str(line), 'req=', ',res=')
        tmp=eval(tmp)
        log.append(tmp)
f.close()

temp=[]
for d in log:
    temp.append([d.get('function_id', 'null'),d.get('chanel_id','null'),d.get('app_id','null'),d.get('op_station','null'),d.get('mobile','null')])
 
data=pd.DataFrame(temp,columns=['function_id','channel_id','app_id','op_station','mobile'])