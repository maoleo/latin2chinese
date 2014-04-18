__author__ = 'joel'
# -*- coding=utf-8 -*-

import math


def Pinyin2Chinese(f_chn2pin):  # f is the original training corpus
    """

    :param f_chn2pin:
    :return:
    """
    D = {'<S>': ['<S>'], '<E>': ['<E>']}
    for line in open(f_chn2pin):
        t = line.split()
        D[t[1]] = t[0]
        D[t[0]] = t[1]
    return D


def tag2tag(f_corpus):
    """

    :param f_corpus:
    """
    fromD = {}
    D = {}

    for line in open(f_corpus):
        pairList = line.split()
        for pair in range(0, len(pairList)):
            pairList[pair] = pairList[pair].split('/')
        for pair in range(0, len(pairList) - 2):
            fromTag = pairList[pair][1]
            transitionTag = fromTag+'|'+pairList[pair + 1][1]
            if not fromTag in fromD:
                fromD[fromTag] = 1.0
            else:
                fromD[fromTag] += 1.0
            if not transitionTag in D:
                D[transitionTag] = 1.0
            else:
                D[transitionTag] += 1.0
    for key in D.keys():
        fromTag = key.split('|')[0][0:]
        D[key] /= fromD[fromTag]
        D[key] = -math.log(D[key])

    return D


def initialPro(f_corpus):
    D = {}
    count = 0.0
    for line in open(f_corpus):
        count += 1.0
        pairList = line.split()
        for pair in range(0, len(pairList)):
            pairList[pair] = pairList[pair].split('/')

        dictKey = pairList[0][1]
        if not dictKey in D:
            D[dictKey] = 1.0
        else:
            D[dictKey] += 1.0

    for tag in D.keys():
        D[tag] /= count
        D[tag] = -math.log(D[tag])

    return D


def emission(f_corpus, Dictionary):
    tagD = {}
    D = {}
    for line in open(f_corpus):
        pairList = line.split()
        for pair in range(0, len(pairList)):
            pairList[pair] = pairList[pair].split('/')
            word = pairList[pair][0]
            tag = pairList[pair][1]
            pinyin = ''
            for i in range(1, len(word)/3):
                if word[(i-1)*3:i*3] in Dictionary:
                    pinyin = pinyin + '/' + Dictionary[word[(i-1)*3:i*3]]
                else:
                    continue
            dictKey = tag + '|' + pinyin

            if not tag in tagD:
                tagD[tag] = 1.0
            else:
                tagD[tag] += 1.0

            if not tag in D:
                D[tag] = {}
                D[tag][dictKey] = 1.0
            else:
                if not dictKey in D[tag]:
                    D[tag][dictKey] = 1.0
                else:
                    D[tag][dictKey] += 1.0

    for tag in D.keys():
        for dictKey in D[tag].keys():
            D[tag][dictKey] /= tagD[tag]
            D[tag][dictKey] = -math.log(D[tag][dictKey])

    return D


def Vocabulary(f_corpus, Dictionary, f_chn2pin):
    D = {}
    countD = {}
    for line in open(f_corpus):
        pairList = line.split()
        for pair in range(0, len(pairList)):
            pairList[pair] = pairList[pair].split('/')
            word = pairList[pair][0]
            pinyin = ''
            newWord = ''
            for i in range(1, len(word)/3):
                if word[(i-1)*3:i*3] in Dictionary:
                    pinyin = pinyin + '/' + Dictionary[word[(i-1)*3:i*3]]
                    newWord += word[(i-1)*3:i*3]
                else:
                    continue

            if not pinyin in D:
                D[pinyin] = {}
                D[pinyin][newWord] = 1.0
                countD[pinyin] = 1.0
            else:
                if not newWord in D[pinyin]:
                    D[pinyin][newWord] = 1.0
                    countD[pinyin] += 1.0
                else:
                    D[pinyin][newWord] += 1.0
                    countD[pinyin] += 1.0

    for line in open(f_chn2pin):
        t = line.split()
        newWord = t[0]
        pinyin = '/'+t[1]

        if not pinyin in D:
                D[pinyin] = {}
                D[pinyin][newWord] = 1.0
                countD[pinyin] = 1.0
        else:
            if not newWord in D[pinyin]:
                D[pinyin][newWord] = 1.0
                countD[pinyin] += 1.0
            else:
                D[pinyin][newWord] += 1.0
                countD[pinyin] += 1.0


    for pinyin in D.keys():
        for dictKey in D[pinyin].keys():
            D[pinyin][dictKey] /= countD[pinyin]
            D[pinyin][dictKey] = -math.log(D[pinyin][dictKey])

    return D



