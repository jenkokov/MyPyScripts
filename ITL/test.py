from time import gmtime, strftime
import requests
import json

url = 'http://app.dev.central.itl/dev1/'


class Workstation():
    def __init__(self, dictionary):
        self.workstation_session_id = dictionary['workstation_session_id']
        self.server_version = dictionary['server_version']
        self.api_protocol_version = dictionary['api_protocol_version']
        self.real_server_url = dictionary['real_server_url']
        self.workstation_id = dictionary['workstation_id']
        self.workstation_num = dictionary['workstation_num']
        self.is_workstation_auto_off = dictionary['is_workstation_auto_off']
        self.workstation_auto_off_timeout = dictionary['workstation_auto_off_timeout']


def send(header, packet):
    operation = dict()
    operation["header"] = header
    operation["request"] = [packet]
    string = "req=" + json.dumps(operation)
    r = requests.post(url, data=string)
    return r.json()


def parse(response):
    resp = response['response'][0]
    if 'error' in resp:
        print 'Error: ' + resp['error']['text'] + '. Code: ' + str(resp['error']['code'])
        return False
    else:
        comp = Workstation(resp['params'][0])
        return comp


def main():
    info_station = workstation_auth()
    if info_station:
        print 'Successful login!\nWorkstation ID: {0}.\nWorkstation session ID: {1}.'.format(info_station.workstation_id, info_station.workstation_session_id)


def workstation_auth():
    time = strftime("%Y-%m-%dT%H:%M:%S", gmtime())
    packet = {'name': 'workstation_auth', 'type': "list", 'namespace': "auth"}
    header = {'user_id': 0, 'session_id': 0, 'request_datetime': time}
    response = send(header, packet)
    return parse(response)


if __name__ == '__main__':
    main()