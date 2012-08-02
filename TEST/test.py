# coding: utf8
import lxml
from lxml import html
artistMas = []

file = open('C:\\Python27\\example\\MyPyScripts\\TEST\\audio4user_7171481.xml')
f = file.read()
doc  = lxml.html.document_fromstring(f)
for artist in doc.cssselect(u'artist'):
    artistMas.append(artist.text)
for i in artistMas:
    print i

