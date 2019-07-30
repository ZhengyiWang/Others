#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 09:26:52 2019

@author: zhengyi_wang
"""

__all__ = ['encode','decode','bbox','neighbors']
_base32 = '0123456789bcdefghjkmnpqrstuvwxyz'
#10进制和32进制转换，32进制去掉了ailo
_decode_map = {}
_encode_map = {}
for i in range(len(_base32)):
    _decode_map[_base32[i]] = i
    _encode_map[i]=_base32[i]
del i

# 交线位置给左下

def decode_exactly(geohash):
    """
    Decode the geohash to its exact values, including the error
    margins of the result.  Returns four float values: latitude,
    longitude, the plus/minus error for latitude (as a positive
    number) and the plus/minus error for longitude (as a positive
    number).
    """
    lat_interval, lon_interval = (-90.0, 90.0), (-180.0, 180.0)
    lat_err, lon_err = 90.0, 180.0
    is_even = True
    for c in geohash:
        cd = _decode_map[c]
        for mask in [16, 8, 4, 2, 1]:
            if is_even: # adds longitude info
                lon_err /= 2
                if cd & mask:
                    lon_interval = ((lon_interval[0]+lon_interval[1])/2, lon_interval[1])
                else:
                    lon_interval = (lon_interval[0], (lon_interval[0]+lon_interval[1])/2)
            else:      # adds latitude info
                lat_err /= 2
                if cd & mask:
                    lat_interval = ((lat_interval[0]+lat_interval[1])/2, lat_interval[1])
                else:
                    lat_interval = (lat_interval[0], (lat_interval[0]+lat_interval[1])/2)
            is_even = not is_even
    lat = (lat_interval[0] + lat_interval[1]) / 2
    lon = (lon_interval[0] + lon_interval[1]) / 2
    return lat, lon, lat_err, lon_err

def decode(geohash):
    lat_range, lon_range = [-90.0, 90.0], [-180.0, 180.0]
    is_lon=True
    for letter in geohash:
        code=str(bin(_decode_map[letter]))[2:].rjust(5,'0')
        for bi in code:
            if is_lon and bi=='0':
                lon_range[1]=sum(lon_range)/2
            elif is_lon and bi=='1':
                lon_range[0]=sum(lon_range)/2
            elif (not is_lon) and bi=='0':
                lat_range[1]=sum(lat_range)/2
            elif (not is_lon) and bi=='1':
                lat_range[0]=sum(lat_range)/2
            is_lon=not is_lon
    return sum(lat_range)/2,sum(lon_range)/2

def encode(lat,lon,precision=12):
    lat_range, lon_range = [-90.0, 90.0], [-180.0, 180.0]
    geohash=[]
    code=[]
    j=0
    while len(geohash)<precision:
#         print(code,lat_range,lon_range,geohash)
        j+=1
        lat_mid=sum(lat_range)/2
        lon_mid=sum(lon_range)/2
        #经度
        if lon<=lon_mid:
            code.append(0)
            lon_range[1]=lon_mid
        else:
            code.append(1)
            lon_range[0]=lon_mid
        #纬度
        if lat<=lat_mid:
            code.append(0)
            lat_range[1]=lat_mid
        else:
            code.append(1)
            lat_range[0]=lat_mid
        ##encode
        if len(code)>=5:
            geohash.append(_encode_map[int(''.join(map(str,code[:5])),2)])
            code=code[5:]
    return ''.join(geohash)



def neighbors(geohash):
    neighbors=[]
    lat_range,lon_range=180,360
    x,y=decode(geohash)
    num=len(geohash)*5
    dx=lat_range/(2**(num//2))
    dy=lon_range/(2**(num-num//2))
    for i in range(1,-2,-1):
        for j in range(-1,2):
            neighbors.append(encode(x+i*dx,y+j*dy,num//5))
#     neighbors.remove(geohash)
    return neighbors

def bbox(geohash):
    lat_range, lon_range = [-90.0, 90.0], [-180.0, 180.0]
    is_lon=True
    for letter in geohash:
        code=str(bin(_decode_map[letter]))[2:].rjust(5,'0')
        for bi in code:
            if is_lon and bi=='0':
                lon_range[1]=sum(lon_range)/2
            elif is_lon and bi=='1':
                lon_range[0]=sum(lon_range)/2
            elif (not is_lon) and bi=='0':
                lat_range[1]=sum(lat_range)/2
            elif (not is_lon) and bi=='1':
                lat_range[0]=sum(lat_range)/2
            is_lon=not is_lon
    #左上、右下；(lat_max,lon_min),(lat_min,lon_max)
    return [(lat_range[1],lon_range[0]),(lat_range[0],lon_range[1])]

