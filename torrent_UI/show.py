import httplib

def printText(txt):
    lines = txt.split('\n')
    for line in lines:
        print line.strip()

httpServ = httplib.HTTPConnection("127.0.0.1", 7755)
httpServ.connect()
#http://127.0.0.1:7755/gui/?list=1
#httpServ.request('GET', "/gui/?list=1")
httpServ.request('GET', "/gui/token.html?t=1351085423565")

response = httpServ.getresponse()
print response.read()
print response.status
'''
if response.status == httplib.OK:
    print "Output from HTML request"
    printText (response.read())

httpServ.request('GET', '/cgi_form.cgi?name=Brad&quote=Testing.')

response = httpServ.getresponse()
if response.status == httplib.OK:
    print "Output from CGI request"
    printText (response.read())
'''
httpServ.close()