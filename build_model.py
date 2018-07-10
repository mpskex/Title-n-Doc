#coding: utf-8
import word2vec
"""
Script for building word2vec model
"""

word2vec.word2vec('corpus_content.txt.seg', 'model_content.bin', size=500,verbose=True)
word2vec.word2vec('corpus_title.txt.seg', 'model_title.bin', size=500,verbose=True)