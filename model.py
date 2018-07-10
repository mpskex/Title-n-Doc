# coding: utf-8
import sys
import jieba
import codecs
import string
import word2vec
from keywords import clean_words, remove_stop, get_keyword
from stop_words import english_stop_words

"""
Preparing segmented data for feeding words to the word2vec module
    mpskex @ github
"""

cache_dir = "data_cache/"
record_list_fname = "record.list.txt"


class w2v_model():

    def __init__(self, record_list_fname, cache_dir, pretrained=None, model_name=None, vec_out=300):
        self.records = None
        self.cache_dir = cache_dir
        self.tmp_file = 'str.tmp'
        self.vec_out = vec_out
        with open(record_list_fname, 'r') as frl:
            self.records = map(lambda x: x.split('\n')[0], frl.readlines())
        #   ++++++++++++++++++++++++++++++
        #   model name
        if model_name is not None:
            self.model_name = model_name
        else:
            self.model_name = 'model'
        #   ++++++++++++++++++++++++++++++
        #   pretrained model
        if pretrained is not None:
            self.model = word2vec.load(pretrained)
        else:
            self.model = self.build_model()
    
    def __load_seg_plainstr(self):
        _str = ''
        lncnt = 0
        for docno in self.records:
            with open(self.cache_dir + docno, 'r') as f:
                with open(self.tmp_file, 'a') as tmp:
                    while(True):
                        r = f.readline()
                        if r is '' or r is None:
                            break
                        ret = clean_words(r, language='Chinese')
                        result = []
                        for te, fl in ret:
                            if fl != "eng":
                                result.append(te)
                        tmp.write(' '.join(result))
                    sys.stdout.write("\r[>>] Parsing %d records..." % (lncnt + 1))
                    lncnt += 1

    def build_model(self):
        self.__load_seg_plainstr()
        word2vec.word2vec(self.tmp_file, self.model_name+'.bin', size=self.vec_out, verbose=True)
        return word2vec.load(self.model_name+'.bin')

# name_list = ['corpus_content_raw.txt', 'corpus_title_raw.txt']


if __name__ == '__main__':
    m = w2v_model(record_list_fname, cache_dir, model_name='1000v500', vec_out=500)
