#coding: utf-8
import math
import operator
import string

#   External Requirement
import jieba
import jieba.posseg as pseg
#   Internal Requirement
from stop_words import english_stop_words

"""
Python version of 
Keyword extraction by entropy difference between the intrinsic and extrinsic mode
Last modified by mpskex (Liu Fangrui) (2018-07-04)
"""
class ParsingException(Exception):
    def __init__(self, err):
        Exception.__init__(self, err)



def remove_stop(text):
    'Remove stop word'
    return [x for x in text if x not in english_stop_words + [""]]


def clean_words(text, language='English'):
    'standardization document: Removing punctuation,all letters lower case'
    delEStr = string.punctuation + string.digits + "–|[：+——！，。？、~@#￥%……&*（）]"
    text = text.replace("\n", " ")
    text = text.replace("\t", " ")
    text = text.replace("\r", " ")
    if language == 'English':
        #   This is caused by obsolete string built-in function implementation
        #   Python 2's api is not built-in and Python 3 is built inside the interpreter
        #   Also the maketrans have changed arg format to (before_char_list, after_char_list)
        #   to establish the mapping between those chars
        '''#   python 2.7+ compatible
        translation = string.maketrans(delEStr, str(" "*len(delEStr)))
        '''
        #   python 3.3+ compatible
        translation = str.maketrans(delEStr, str(" "*len(delEStr)))
        text = text.translate(translation)  # Remove punctuation and numbers
        text = text.lower()
        #   English words seperated by spaces
        text = text.split(' ')
    elif language == 'Chinese':
        """
        Chinese serialization returns pair of (word, flag)
        """
        #   Full width comma
        delEStr += "＂“”［ ］【】，。/？！……～·、」「《》；： ．ＡＢＣＤＥＦＧＨＩＪＫＭＮＯＰＱＲＳＴＵＶＷＸＹＺａｂｃｄｅｆｇｈｉｊｋｍｎｏｐｑｒｓｔｕｖｗｘｙｚ１２３４５６７８９０"
        translation = str.maketrans(delEStr, str("\0"*len(delEStr)))
        text = text.translate(translation)  # Remove punctuation and numbers
        text = list(text)
        for spc in ['', ' ', '\0']:
            for idx in range(text.count(spc)):
                text.remove(spc)
        text = ''.join(text)
        text = pseg.lcut(text)
    else:
        raise NotImplementedError
    if text is [] or text is None:
        raise ParsingException("No Chinese Detected")
    return text


def get_keyword(text):
    l = len(text)
    location = {}
    distance = {}
    for i, word in enumerate(text, 0):
        if word not in list(location.keys()):
            location[word] = i
            distance[word] = [i]
        else:
            distance[word].append(i - location[word])
            location[word] = i
    for word in list(distance.keys()):
        distance[word].append(l - location[word] + distance[word][0])
        distance[word].remove(distance[word][0])

    # print(distance['sterility'])
    # print(len(distance['sterility']))

    value = {}
    for word in list(set(text)):
        # print(word)
        # word = 'sterility'
        intrinsic = {}
        extrinsic = {}
        mean = 1.0 * l / len(distance[word])
        # print 'mean:',mean
        for num in distance[word]:
            if num <= mean:
                intrinsic[num] = 1
            else:
                extrinsic[num] = 1
        # print len(intrinsic),len(extrinsic)
        H_dI = math.log(len(intrinsic), 2) if len(intrinsic) != 0 else 0
        H_dE = math.log(len(extrinsic), 2) if len(extrinsic) != 0 else 0
        EDq_d = H_dI**2 - H_dE**2
        # print 'H_dI:',H_dI
        # print 'H_dE:',H_dE
        # print 'EDq_d:',EDq_d
        pI = 0
        Hgeo_dI = 0.0
        Hgeo_dE = 0.0
        try:
            for i in range(1, int(mean)):
                pI += (1 / mean) * math.pow(1 - 1 / mean, i - 1)
            for i in range(1, int(mean)):
                Hgeo_dI += -(
                    (1 / mean) * math.pow(1 - 1 / mean, i - 1)) / pI * math.log(
                        ((1 / mean) * math.pow(1 - 1 / mean, i - 1)) / pI, 2)
            pE = 1 - pI
            for i in range(int(mean), l):
                Hgeo_dE += -(
                    (1 / mean) * math.pow(1 - 1 / mean, i - 1)) / pE * math.log(
                        ((1 / mean) * math.pow(1 - 1 / mean, i - 1)) / pE, 2)
            EDgeoq_d = Hgeo_dI**2 - Hgeo_dE**2
            EDnorq_d = EDq_d / abs(EDgeoq_d) if abs(EDgeoq_d) != 0 else -1000
        except Exception as err:
            EDnorq_d = -1000
        # print('Hgeo_dI:',Hgeo_dI)
        # print('Hgeo_dE:',Hgeo_dE)
        value[word] = EDnorq_d
        # print(word, EDnorq_d)
    # print('Calculate Over...')
    v = sorted(list(value.items()), key=operator.itemgetter(1), reverse=True)
    return v

if __name__ == '__main__':
    """
    Self keyword extraction testing
    """
    with open('keywords.py', 'r') as f:
        print(get_keyword(remove_stop(clean_words(f.read())))[:])
        f.close()

