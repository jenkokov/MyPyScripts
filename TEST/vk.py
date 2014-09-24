import cookielib
import urllib2
import urllib
from urlparse import urlparse
from HTMLParser import HTMLParser
import webbrowser
import vk_auth
import json
from pprint import pprint



def auth_user(email, password, client_id, scope, opener):
    #response = opener.open(
    #    "http://oauth.vk.com/oauth/authorize?" +\
    #    "redirect_uri=http://oauth.vk.com/blank.html&response_type=token&" +\
    #    "client_id=%s&scope=%s&display=popup" % (client_id, ",".join(scope)))
    #doc = response.read()
    res = urllib2.urlopen("http://oauth.vk.com/oauth/authorize?" +\
                          "redirect_uri=http://oauth.vk.com/blank.html&response_type=token&" +\
                          "client_id=%s&scope=%s&display=popup" % (client_id, ",".join(scope)))

    webbrowser.open_new("http://oauth.vk.com/oauth/authorize?" +\
                    "redirect_uri=http://oauth.vk.com/blank.html&response_type=token&" +\
                    "client_id=%s&scope=%s&display=page" % (client_id, ",".join(scope)))
    #print doc


def main():
    data = {}
    data['uids'] = '7171481'
    data['fields'] = 'online'
    data['name_case'] = 'nom'
    data['access_token']='ac37ae23bbc1dc1dc92c3b4eee85fcafcf257130b2db86a3ef9dc5c4848efec4ef95f3adc671a03cd00d1'
    url_values = urllib.urlencode(data)
    url = 'https://api.vk.com/method/getProfiles'
    full_url = url + '?' + url_values
    print full_url
    data = urllib2.urlopen(full_url)
    i = data.read()
    print json.dumps(i,encoding='UTF-8')
    json.JSONEncoder.encode(i)


    pass

if __name__ == '__main__':
    email = 'jenko.kov@gmail.com'
    password = 'TESTPASS'
    opener = urllib2.build_opener(
    urllib2.HTTPCookieProcessor(cookielib.CookieJar()),
    urllib2.HTTPRedirectHandler())
    clien_id = '3309463'
    scope = 'friends'
    #auth_user(email,password,clien_id,scope,opener)
    main()

