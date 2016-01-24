#coding:utf-8

text = '''
This is test about the python file and input output
.
..
...
....
.....
......
.......
........
'''

f = file('what.txt', 'w')
f.write(text)
f.close()

f = file('what.txt')
while True:
	line = f.readline()
	if len(line) == 0:
		break
	print line

f.close()
# file方法获取对象，读或写
# write readline 方法 close 方法


# ========== pickle ========

import pickle as p

shoplistfile = 'shoplist.data'
shoplist = ['Macbook pro', 'Sureface book', 'Chromebook pixel']

f = file(shoplistfile, 'w')
p.dump(shoplist, f)
f.close()

f = file(shoplistfile)
l = p.load(f)
print l

# import ... as ...  为了方便书写
# dump 和 load 两个方法











