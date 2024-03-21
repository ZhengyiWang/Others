# -*- coding: utf-8 -*-
"""
Created on Fri May  7 15:13:32 2021

@author: dell
"""

import csv

word_dict=[]
field_name=[]

#读取已有词根词缀
csvFile = open("C:\\Users\\dell\\Desktop\\dict.csv", "r")
reader = csv.reader(csvFile)

# 建立空字典
replacements = {}
for item in reader:
    # 忽略第一行
    if reader.line_num == 1:
        continue
    replacements[item[0]] = item[1]

csvFile.close()

word_dict=[x for x in replacements.keys()]

#读取待翻译字段名
with open("C:\\Users\dell\Desktop\\field name.txt", "r",encoding='UTF-8') as f:
	for line in f:
		field_name.append(line.strip('\n'))
                

## leetcode 140  
#DFS: time: O(2^n), space: O(n)
#DP: time: O(n^2*k), space: O(nk), 假设k表示平均每个长度对应解的个数

def wordBreak(s, wordDict):
    mem_ = {}

    def dfs(s, wordDict):
        if s in mem_:
            return mem_[s]
        ans = [] # answer for curr s
        if s in wordDict:
            ans.append(s)
            
             
        min_index=len(s)+1
        s_tmp=s
        for w in wordDict:
            if s.find(w)!=-1 and s.find(w)<min_index:
                min_index=s.find(w)
        s=s_tmp[min_index:]

        
        for j in range(1, len(s)):
             left = s[:j]
             if left not in wordDict:
                 continue
             right = s[j:]
             left_ans = [' '+left + ' ' + x for x in dfs(right, wordDict)]
             ans += left_ans
        if len(ans) == 0:
            ans.append(s)
        mem_[s] = ans
        return mem_[s]
    
    return dfs(s, wordDict)

##需要人工调整分词结果##
res=[]
for f in field_name:
    res.append(wordBreak(f,word_dict))



res_fin=[]
for r in res:
    res_fin.append(r[0].strip(" ").split(" "))
    
for rr in res_fin:
    for w in rr:
        if w=='':
            rr.remove(w)
        
#替换单词  #可以优化为一个dict  方便比较
final_result=[]
for f_test in field_name:
    for r in res_fin:
        for w in r:
            f_test=f_test.replace(w,replacements[w],1)
    final_result.append(f_test)


with open("C:\\Users\dell\Desktop\\final_rest.txt", 'w') as f:
    for item in final_result:
        f.write("%s \n" % item)        