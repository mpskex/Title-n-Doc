# coding: utf-8
import sys
import jieba
import codecs
import string
import numpy as np
import word2vec
from distance import euclid_dist, cosine, hausdorff_dist, mean, var
from keywords import clean_words, remove_stop, get_keyword, ParsingException
from stop_words import english_stop_words

"""
Preparing segmented data for feeding words to the word2vec module
    mpskex @ github
"""

cache_dir = "data_cache/"
record_list_fname = "record.list.txt"


class w2v_model():

    def __init__(self, record_list_fname=None, cache_dir=None, pretrained=None, model_name='model', vec_out=300):
        self.vec_out = vec_out
        #   ++++++++++++++++++++++++++++++
        #   model name
        self.model_name = model_name
        #   ++++++++++++++++++++++++++++++
        #   pretrained model
        if pretrained is not None or not '':
            self.model = word2vec.load(pretrained+'.bin')
        else:
            if record_list_fname is None or cache_dir is None:
                raise ValueError("Record and Cache directory should be given if pretrain model dir is not set!")
            self.model = self.build_model(record_list_fname, cache_dir, 'str.tmp')
        print("[*]\tInitialization Complete!")
    
    def __load_seg_plainstr(self, record_list_fname, cache_dir, tmp_file):
        _str = ''
        lncnt = 0
        records = None
        with open(record_list_fname, 'r') as frl:
            records = map(lambda x: x.split('\n')[0], frl.readlines())
        if records == []:
            raise ValueError("No Records ID Recieved in __load_seg_plainstr()!")
        for docno in records:
            with open(cache_dir + docno, 'r') as f:
                with open(tmp_file, 'a') as tmp:
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

    def build_model(self, record_list_fname, cache_dir, tmp_file):
        self.__load_seg_plainstr(record_list_fname, cache_dir, tmp_file)
        word2vec.word2vec(tmp_file, self.model_name + '.bin', size=self.vec_out, verbose=True)
        return word2vec.load(self.model_name + '.bin')
    
    def get_vec(self, word):
        try:
            return self.model[word]
        except KeyError as e:
            print("[!]\tError: No Key Value ", e)
            return None
    
    def dist_docs(self, str_a, str_b, method='mean_euclid', keyword_ex=False,  debug=False):
        pair_a = clean_words(str_a, language='Chinese')
        pair_b = clean_words(str_b, language='Chinese')
        wordbag_a = []
        wordbag_b = []
        for te, fl in pair_a:
            if fl != "eng":
                wordbag_a.append(te)
        for te, fl in pair_b:
            if fl != "eng":
                wordbag_b.append(te)
        if debug:
            for bag in [wordbag_a, wordbag_b]:
                print('\ '.join(bag))
        print("[*]\tParsed two string!")
        vecbag_a = []
        vecbag_b = []
        for word in wordbag_a:
            vec = self.get_vec(word)
            if vec is None:
                continue
            else:
                vecbag_a.append(vec)
        for word in wordbag_b:
            vec = self.get_vec(word)
            if vec is None:
                continue
            else:
                vecbag_b.append(vec)
        vecbag_a = np.array(vecbag_a)
        vecbag_b = np.array(vecbag_b)
        if debug:
            for bag in [vecbag_a, vecbag_b]:
                print(bag.shape)
        for bag in [vecbag_a, vecbag_b]:
            for word in bag:
                if len(word.shape) == 0:
                    bag.remove(word)
        if (vecbag_a==None).all() or (vecbag_b==None).all():
            raise ParsingException("No Chinese phrase extracted!!")
        if method == 'mean_euclid':
            mean_a = np.mean(vecbag_a, axis=0)
            mean_b = np.mean(vecbag_b, axis=0)
            if debug:
                for vec in [mean_a, mean_b]:
                    print(vec.shape)
            dist = euclid_dist(mean_a, mean_b)
            if debug:
                print(dist)
            return dist
        else:
            raise NotImplementedError

if __name__ == '__main__':
    #   Little demo to create model
    model_name = '1000v500'
    #   m = w2v_model(record_list_fname, cache_dir, model_name=model_name, vec_out=500)
    m = w2v_model(pretrained=model_name)
    indexes = m.model.cosine(u'加拿大')
    for index in indexes[0]:
        print(m.model.vocab[index])
    m.get_vec(u'牛逼')
    m.dist_docs(u'自定义的异常类必须是Exception或者Error的子类！', u'使用raise语句来引发一个异常，其中check_positive_int(para_list)函数是用来检查输入的list是否为正整数。', debug=True)