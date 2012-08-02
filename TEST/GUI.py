# coding: utf8
import urllib2
import lxml
from lxml import html
import os

def ex(event):
    sys.exit()

def download(i):
    file_size_dl = 0
    block_sz = 8192
    #for i in info:
    a=i.split(';;')
    filename = a[0] + ' - '+a[1]+'.mp3'
    if len(filename) > 60:
        filename=filename[:60]+'.mp3'
    url=a[2]
    u = urllib2.urlopen(url)
    meta = u.info()
    file_size = int(meta.getheaders("Content-Length")[0])
    if os.path.exists(folder.get()+filename):
        print u'File {0} already exist!'.format(filename)
        real_size=os.path.getsize(folder.get()+filename)
        if real_size == file_size:
            return
    if  os.path.exists(folder.get()+url.split('/')[-1]):
        print u'File {0} already exist!'.format(filename)
        real_size=os.path.getsize(folder.get()+url.split('/')[-1])
        if real_size == file_size:
            return
    try:
        f = open(folder.get()+filename, 'wb')
    except :
        f = open(folder.get()+url.split('/')[-1], 'wb')
    print 'Downloading '+ filename + '\nSize: '+str(file_size)
    status.config(text='Downloading '+ filename + '\nSize: '+str(file_size))
    tex.delete(1.0,END)
    tex.insert(END,filename)
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break

        file_size_dl += len(buffer)
        f.write(buffer)

def parse(file):
    number=0
    doc  = lxml.html.document_fromstring(file)
    for artist in doc.cssselect('artist'):
        artistMas.append(artist.text)
        number = number + 1
    for title in doc.cssselect('title'):
        titleMas.append(title.text)
    for urlm in doc.cssselect('url'):
        urlMas.append(urlm.text)
    for i in xrange(0, number):
        summary.append(artistMas[i]+';;'+titleMas[i]+';;'+urlMas[i])
    return summary


def output(event):
    status.config(text='Downloading...')
    t = token.get()
    id_user = id.get()
    f = folder.get()
    if not os.path.exists(f):
        os.makedirs(f)
    print f
    tex.delete(1.0,END)
    tex.insert(END,"Token: {0}\nUser ID: {1}\nFolder: {2}".format(t,id_user,f))
    url = "https://api.vkontakte.ru/method/audio.get.xml?uid=" + id_user + "&access_token=" + t
    page = urllib2.urlopen(url)
    html = page.read()
    dict = parse(html)
    for a in dict:
        download(a)
    #    print u'Artist: {0}\tSong: {1}\tURL: {2}'.format(i[0],i[1],i[2])
    #f = open('audio4user_{0}.xml'.format(id_user),'wb')
    #f.write(html)
    #f.close()



from Tkinter import *
root = Tk()

artistMas = []
titleMas = []
urlMas = []
summary=[]
dict=[]
number = 0

status= Label(root, text = 'Ready!', height=2)
token_label=Label(root, text = 'Token:')
token = Entry(root,width=30)
token.insert(0,'1f0a1e304f7b72a91f3f22559d1f469ded11f6b1f6773a17ba207024c543f4d')
id_label=Label(root, text = 'User ID:')
id = Entry(root,width=30)
id.insert(0,'7171481')
folder_label=Label(root, text = 'Folder:')
folder = Entry(root,width=30)
folder.insert(0,'C:\\Downloads\\VKMusic\\')
but = Button(root,text="Output")
tex = Text(root,width=20,height=3,font="12",wrap=WORD)

token.grid(row=0,column=1,padx=20)
token_label.grid(row=0, column=0)
id_label.grid(row=1,column=0)
id.grid(row=1,column=1,padx=20)
folder_label.grid(row=2,column=0)
folder.grid(row=2,column=1,padx=20)
but.grid(row=1,column=2)
tex.grid(row=1,column=3,padx=10,pady=10)
status.grid(row=0,column=3)

root.bind("<Return>",output)
#root.bind("<space>",ex)
but.bind("<Button-1>",output)

root.mainloop() 