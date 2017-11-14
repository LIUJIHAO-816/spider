__author__ = 'Liujuhao'
import json

f = open('e://china/data.json','r')
str = f.read()
dict = json.loads(str)
print str
print dict
print type(str)
print type(dict)
f.close()