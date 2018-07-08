#coding: utf-8
import word2vec

model = word2vec.load('model_content.bin')
indexes = model.cosine(u'孤儿')
for index in indexes[0]:
    print (model.vocab[index])