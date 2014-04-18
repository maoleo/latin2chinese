__author__ = 'joel'

import shelve
import py2cnStr

db = {}
print('Loading language model...')
Database = shelve.open('DB')
db['D_py2ch'] = Database['D_py2ch']
db['transition'] = Database['transition']
db['initial'] = Database['initial']
db['emission'] = Database['emission']
db['vocabulary'] = Database['vocabulary']
Database.close()
print('Finish')

for line in open('test'):
    print('*The original sentence we get:')
    print(line)
    pinyin = []
    Chinese_ori = line
    for i in range(0, len(Chinese_ori)/3):
        word = Chinese_ori[i*3:(i+1)*3]
        if word in db['D_py2ch'].keys():
            pinyin.append(db['D_py2ch'][word])
        else:
            continue

    # print('The pinyin we get:')
    # print(pinyin)

    Chinese = py2cnStr.translate(db, pinyin)

    print('*The translation we get:')
    print(Chinese)
    print('*************************************************************************')



