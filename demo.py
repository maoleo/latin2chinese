__author__ = 'joel'
# -*- coding=utf-8 -*-
import shelve
import py2cnStr

if __name__ == '__main__':

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
    print('')
    print('Please type in pinyin，use space to split，like "wo ai ke da";\nUSE [q]uit to quit')

    while 1:
        py = raw_input()
        if py == "q":
            break
        if py == " ":
            continue

        print('Input pinyin is:')
        print(py)

        chinese = py2cnStr.translate(db, py.split())
        print('Output Chinese is:')
        print(chinese)



