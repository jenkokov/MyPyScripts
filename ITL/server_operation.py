import json
from time import strftime, gmtime
import requests
from test_client import *

url = 'http://app.dev.central.itl/dev1/'


def status_check(workstation_session_id):
    time = strftime("%Y-%m-%dT%H:%M:%S", gmtime())
    params = {'workstation_session_id': workstation_session_id}
    packet = {'name': 'status_check', 'type': "list", 'namespace': "service", 'params': params}
    header = {'user_id': 0, 'session_id': 0, 'request_datetime': time}
    return parse(send(header, packet))


def workstation_auth():
    time = strftime("%Y-%m-%dT%H:%M:%S", gmtime())
    packet = {'name': 'workstation_auth', 'type': "list", 'namespace': "auth"}
    header = {'user_id': 0, 'session_id': 0, 'request_datetime': time}
    return parse(send(header, packet))


def workstation_disconnect(workstation_session_id):
    time = strftime("%Y-%m-%dT%H:%M:%S", gmtime())
    params = {'workstation_session_id': workstation_session_id}
    packet = {'name': 'workstation_disconnect', 'type': "list", 'namespace': "auth", 'params': params}
    header = {'user_id': 0, 'session_id': 0, 'request_datetime': time}
    print 'Disconnect workstation. Close session with ID {0}.'.format(workstation_session_id)
    return parse(send(header, packet))


def user_auth(login, password, session_type):
    time = strftime("%Y-%m-%dT%H:%M:%S", gmtime())
    params = {'login': login, 'pass': password, 'session_type': session_type}
    packet = {'name': 'user_auth', 'type': "list", 'namespace': "auth", 'params': params}
    header = {'user_id': 0, 'session_id': 0, 'request_datetime': time}
    return parse(send(header, packet))


def user_disconnect(session_id, user_id):
    time = strftime("%Y-%m-%dT%H:%M:%S", gmtime())
    params = dict()
    packet = {'name': 'user_disconnect', 'type': "list", 'namespace': "auth", 'params': params}
    header = {'user_id': user_id, 'session_id': session_id, 'request_datetime': time}
    print 'Logoff userID {0}.'.format(user_id)
    return parse(send(header, packet))


def send(header, packet):
    operation = dict()
    operation["header"] = header
    operation["request"] = [packet]
    string = "req=" + json.dumps(operation)
    r = requests.post(url, data=string)
    #print string
    try:
        return r.json()
    except:
        print 'No JSON response from server.'
        return False

if __name__ == '__main__':
    print 'System file! Can\'t run.'