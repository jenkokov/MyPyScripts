import json
from time import strftime, gmtime
import requests
from test_client import *
from time import clock
import mysqlitl

settings = mysqlitl.get_settings()
basic_url = settings['basic_url']
get_user_url = settings['get_user_url']


def status_check(workstation_session_id, user_id=0, session_id=0):
    time = strftime("%Y-%m-%dT%H:%M:%S", gmtime())
    params = {'workstation_session_id': workstation_session_id}
    packet = {'name': 'status_check', 'type': "list", 'namespace': "service", 'params': params}
    header = {'user_id': user_id, 'session_id': session_id, 'request_datetime': time}
    t1 = clock()
    return parse(send(header, packet)), clock() - t1


def application_action(session_id, user_id, type_operation, content_id):
    time = strftime("%Y-%m-%dT%H:%M:%S", gmtime())
    if type_operation == 'stop':
        params = {'type': type_operation, 'dic_content_action_id': content_id}
    else:
        params = {'type': type_operation, 'dic_content_id': content_id}
    packet = {'name': 'application_action', 'type': "list", 'namespace': "shell", 'params': params}
    header = {'user_id': user_id, 'session_id': session_id, 'request_datetime': time}
    t1 = clock()
    return parse(send(header, packet)), clock() - t1


def workstation_auth():
    time = strftime("%Y-%m-%dT%H:%M:%S", gmtime())
    packet = {'name': 'workstation_auth', 'type': "list", 'namespace': "auth"}
    header = {'user_id': 0, 'session_id': 0, 'request_datetime': time}
    t1 = clock()
    return parse(send(header, packet)), clock() - t1


def workstation_disconnect(workstation_session_id):
    time = strftime("%Y-%m-%dT%H:%M:%S", gmtime())
    params = {'workstation_session_id': workstation_session_id}
    packet = {'name': 'workstation_disconnect', 'type': "list", 'namespace': "auth", 'params': params}
    header = {'user_id': 0, 'session_id': 0, 'request_datetime': time}
    t1 = clock()
    return parse(send(header, packet)), clock() - t1


def user_auth(login, password, session_type):
    time = strftime("%Y-%m-%dT%H:%M:%S", gmtime())
    params = {'login': login, 'pass': password, 'session_type': session_type}
    packet = {'name': 'user_auth', 'type': "list", 'namespace': "auth", 'params': params}
    header = {'user_id': 0, 'session_id': 0, 'request_datetime': time}
    t1 = clock()
    return parse(send(header, packet)), clock() - t1


def user_disconnect(session_id, user_id):
    time = strftime("%Y-%m-%dT%H:%M:%S", gmtime())
    params = dict()
    packet = {'name': 'user_disconnect', 'type': "list", 'namespace': "auth", 'params': params}
    header = {'user_id': user_id, 'session_id': session_id, 'request_datetime': time}
    t1 = clock()
    return parse(send(header, packet)), clock() - t1


def reg_file_list(session_id, user_id):
    time = strftime("%Y-%m-%dT%H:%M:%S", gmtime())
    params = dict()
    packet = {'name': 'reg_file_list', 'type': "list", 'namespace': "shell", 'params': params}
    header = {'user_id': user_id, 'session_id': session_id, 'request_datetime': time}
    req = send(header, packet)
    return parse(req)


def content_list(session_id, user_id):
    time = strftime("%Y-%m-%dT%H:%M:%S", gmtime())
    params = dict()
    packet = {'name': 'content_list', 'type': "list", 'namespace': "shell", 'params': params}
    header = {'user_id': user_id, 'session_id': session_id, 'request_datetime': time}
    t1 = clock()
    return send(header, packet), clock() - t1


def get_user():
    time = strftime("%Y-%m-%dT%H:%M:%S", gmtime())
    params = dict()
    packet = {"namespace": "user_gen", "type": "list", "name": "get_user", "params": params}
    header = {'user_id': 0, 'session_id': 0, 'request_datetime': time}
    return parse(send(header, packet, get_user_url))


def init_user():
    time = strftime("%Y-%m-%dT%H:%M:%S", gmtime())
    params = dict()
    packet = {"namespace": "user_gen", "type": "list", "name": "init_user", "params": params}
    header = {'user_id': 0, 'session_id': 0, 'request_datetime': time}
    return parse(send(header, packet, get_user_url))


def send(header, packet, url=basic_url):
    operation = dict()
    operation["header"] = header
    operation["request"] = [packet]
    string = "req=" + json.dumps(operation)
    r = requests.post(url, data=string)
    print string
    try:
        return r.json()
    except:
        print 'No JSON response from server.'
        return False

if __name__ == '__main__':
    init_user()
    print 'Init user.'