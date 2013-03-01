import json
from time import strftime, gmtime
import requests
from ITL.test_client import *

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


def workstation_disconnect():
    time = strftime("%Y-%m-%dT%H:%M:%S", gmtime())
    packet = {'name': 'workstation_disconnect', 'type': "list", 'namespace': "auth"}
    header = {'user_id': 0, 'session_id': 0, 'request_datetime': time}
    print parse(send(header, packet))
    print 'Disconnected!'


def send(header, packet):
    operation = dict()
    operation["header"] = header
    operation["request"] = [packet]
    string = "req=" + json.dumps(operation)
    r = requests.post(url, data=string)
    return r.json()