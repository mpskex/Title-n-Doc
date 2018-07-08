# coding: utf-8
import jieba
import codecs
import string
from keywords import clean_words, remove_stop, get_keyword
from stop_words import english_stop_words


with open('test.txt', 'r') as f:
    text = []
    ret = clean_words(f.read(), language='Chinese')
    result = []
    for te, fl in ret:
        if fl != "eng":
            result.append(te)
    print('\ '.join(result))
