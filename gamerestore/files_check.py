import os
import hashlib
from lxml import etree
import sys
import time
import zlib

def get_md5(filename):
    md5 = hashlib.md5()
    with open(filename,'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            md5.update(chunk)
    return md5.hexdigest()

def get_crc(filename):
    return zlib.crc32(open(filename, 'rb').read())

def main(path):
    old = time.time()
    print path
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            md5_hash=str(get_crc(fp))
            d[fp]=md5_hash
            root=etree.Element('file')
            root.set('path',fp)
            #etree.SubElement(root, "filepath").text = fp
            etree.SubElement(root, "md5").text = md5_hash
            print etree.tostring(root,pretty_print=True)
            print time.time()-old
            #print fp,md5_hash
    #print d


if __name__=='__main__':
    path = 'D:\\Games\\Steam\\steamapps\\common\\dota 2 beta'
    d={}
    main(path)