#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 16:01:47 2019

@author: zhengyi_wang
"""

from shapely import geometry
import polygon_geohasher 

import json
#这个需要根据实际的geojson文件进行修改
with open("Zhongshen.geojson",'r') as load_f:
     location = json.load(load_f)['features'][0]['geometry']['coordinates']
location=location[0]

#根据坐标，生成相应的多边形（Shapely's Polygon对象）
test_polygon = geometry.Polygon(location)

#生成geohash
geohash=list(polygon_geohasher.polygon_to_geohashes(test_polygon, 7, False))

#将geohash写入文件
with open ('/Users/zhengyi_wang/Desktop/test.txt','w') as f:
    for g in geohash:
        f.write(g)
        f.write(",")
        
"""
计算凸包并返回geohash
from scipy.spatial import ConvexHull
hull = ConvexHull(location)
hull1=hull.vertices.tolist()#hull.vertices 得到凸轮廓坐标的索引值
new_location=[location[t] for t in hull1 ]
test_polygon_1 = geometry.Polygon(new_location)
geohash_1=list(polygon_geohasher.polygon_to_geohashes(test_polygon_1, 7, False))
print(geohash_1)
"""
