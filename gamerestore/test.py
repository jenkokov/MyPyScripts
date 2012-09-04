from lxml import etree

def main():
    print 'ok!'
    root=etree.Element('LOG')
    etree.SubElement(root, "filepath").text = "D:\\log\\Dlog.txt"
    etree.SubElement(root, "md5").text = "md5hash"
    print etree.tostring(root,pretty_print=True)


if __name__=='__main__':
    main()