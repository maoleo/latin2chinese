__author__ = 'joel'
# -*- coding=utf-8 -*-

import shelve
import readDB

file_hz2py = 'hz2py'
file_corpus = 'corpus_ori'

db = shelve.open('DB')

Dictionary = readDB.Pinyin2Chinese(file_hz2py)
db['D_py2ch'] = Dictionary
# import the Pinyin2Chinese Dictionary

Transition_matrix = readDB.tag2tag(file_corpus
db['transition'] = Transition_matrix

Initial_probabilities = readDB.initialPro(file_corpus)
db['initial'] = Initial_probabilities

Emission_matrix = readDB.emission(file_corpus, Dictionary)
db['emission'] = Emission_matrix

Vocabulary = readDB.Vocabulary(file_corpus, Dictionary, file_hz2py)
db['vocabulary'] = Vocabulary


db.close()

