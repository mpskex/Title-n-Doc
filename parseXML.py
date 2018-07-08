# coding: utf-8
import re
import sys
  
if __name__ == "__main__":
    name = "news_sohusite_xml.smarty.dat"
    # name = "news_sohusite_xml_utf8.dat"
    # name = "SogouCS.WWW08.txt"
    titles = []
    contents = []
    #   record_len      2012 - 6 | 2008 - 8
    #   title_prefix    2012 - 3 | 2008 - 3
    #   content_prefix  2012 - 4 | 2008 - 5
    record_len = 6
    title_prefix = 3
    content_prefix = 4
    with open(name) as f:
        lncnt = 0
        rccnt = 0
        lines = f.readlines()
        print("[*]\tRead ", len(lines), " lines!")
        for line in lines:
            if lncnt == record_len * rccnt + title_prefix:
                titl = (line.split('<contenttitle>')[-1]).split('</contenttitle>')[0]
                titles.append(titl)
                # titl=re.sub(u"[\x00-\x08\x0b-\x0c\x0e-\x1f]+",u"",titl)
                # print(titl)
            elif lncnt == record_len * rccnt + content_prefix:
                cont = line.split('\n')[0]
                cont = (cont.split('<content>')[-1]).split('</content>')[0]
                # cont=re.sub(u"[\x00-\x08\x0b-\x0c\x0e-\x1f]+",u"",cont)
                contents.append(cont)
            elif lncnt == record_len * rccnt + record_len - 1:
                rccnt += 1
            elif lncnt % 100 == 0:
                sys.stdout.write("\r[>>] Parsing in  ... %.2f%%  " % ((lncnt + 1) * 100 / float(len(lines))))
            lncnt += 1
    with open("corpus_title.txt", 'w') as ft:
        ft.write('\n'.join(titles))
    print("[*]\write titles!")
    with open("corpus_content.txt", 'w') as fc:
        fc.writelines('\n'.join(contents))
    print("[*]\write contents!")
        
