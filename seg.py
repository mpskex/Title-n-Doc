#coding: utf-8
import sys
import jieba
import codecs
import string
from keywords import clean_words, remove_stop, get_keyword
from stop_words import english_stop_words

name_list = ['corpus_content_raw.txt', 'corpus_title_raw.txt']

for name in name_list:
    print("[*]\tProcessing file %s..."%(name))
    with open(name, 'r') as f:
        with open(name+'.seg', 'w') as fseg:
            fseg.close()
        with open(name+'.seg', 'a') as fseg:
            cnt = 0
            while True:
                line = f.readline()
                if line is None or line is '':
                    break
                ret = clean_words(line, language='Chinese')
                result = []
                for te, fl in ret:
                    if fl != "eng":
                        result.append(te)
                fseg.write(' '.join(result) + ' ')
                cnt += 1
                sys.stdout.write("\r[>>] Have parsed %d lines" % (cnt))
    print("\n")