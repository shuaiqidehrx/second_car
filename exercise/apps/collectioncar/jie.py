# -*- coding:utf-8 -*-
import jieba

str = '炫酷的跑车'
result = jieba.cut(str,cut_all=False)
print(result)

for i in result:
    print(i)