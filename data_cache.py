# coding: utf-8
import re
import sys
from keywords import clean_words, remove_stop, get_keyword
from stop_words import english_stop_words

"""
Seperate XML format data to raw-independent files 
    -   content.txt
    -   
"""

iter_num = 1000


cache_dir = "data_cache/"
record_list_fname = "record.list"
# name = "news_sohusite_xml.smarty.dat"
name = "news_sohusite_xml_utf8.dat"
# name = "SogouCS.WWW08.txt"


class Record():

    def __init__(self):
        self.docno = None
        self.content = None
        self.title = None

    def isNotNone(self):
        if self.docno is not None and \
            self.content is not None and \
            self.title is not None:
            return True
        else:
            return False

  
if __name__ == "__main__":
    titles = []
    contents = []
    docnos = []
    #   record_len      2012 - 6 | 2008 - 8
    #   title_prefix    2012 - 3 | 2008 - 3
    #   content_prefix  2012 - 4 | 2008 - 5
    record_len = 6
    id_prefix = 2
    title_prefix = 3
    content_prefix = 4
    with open(record_list_fname, "w") as flist:
        flist.close()
    with open(name) as f:
        lncnt = 0
        rccnt = 0
        for i in range(iter_num):
            line = f.readline()
            if line is None or line is '':
                break
            #   Parsing single record
            r = Record()
            for offset in range(1, record_len):
                line = f.readline()
                if line is None or line is '':
                    print("[!]\tNone Read...exited!")
                    break
                if offset == id_prefix:
                    docno = (line.split('<docno>')[-1]).split('</docno>')[0]
                    r.docno = docno
                    docnos.append(docno)
                    # print(docno)
                if offset == title_prefix:
                    titl = (line.split('<contenttitle>')[-1]).split('</contenttitle>')[0]
                    r.title = titl
                    # titl=re.sub(u"[\x00-\x08\x0b-\x0c\x0e-\x1f]+",u"",titl)
                    # titles.append(titl)
                    # print(titl)
                if offset == content_prefix:
                    cont = line.split('\n')[0]
                    cont = (cont.split('<content>')[-1]).split('</content>')[0]
                    r.content = cont
                    # cont=re.sub(u"[\x00-\x08\x0b-\x0c\x0e-\x1f]+",u"",cont)
                    # contents.append(cont)
                    # print(cont)
            if r.isNotNone():
                #   flush it to cache
                with open(cache_dir + r.docno, 'w') as recf:
                    # print(r.title, '\n', r.content)
                    recf.write(r.title + '\n' + r.content)
                    recf.close()
                with open(record_list_fname, 'a') as frl:
                    frl.write(r.docno + '\n')
                    frl.close()
            if lncnt % 100 == 0:
                sys.stdout.write("\r[>>] Parsing %d lines..." % (lncnt + 1))
            lncnt += record_len - 1
            # break
        print("\r[*] Parsed %d lines!     " % (lncnt))
        '''
        with open(record_list_fname, 'w') as frl:
            frl.write('\n'.join(docnos))
        print("[*]\twrite titles!")
        '''
            
