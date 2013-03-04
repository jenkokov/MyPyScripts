from time import sleep
import logging
import os
from server_operation import *
import hashlib

general_log = 'C:\\dslogon\\general.log'
if not os.path.exists('C:\\dslogon\\'):
    os.makedirs('C:\\dslogon\\')
    f = open(general_log, 'a')
    f.close()
logging.basicConfig(filename=general_log, level=logging.INFO,
                    format='%(asctime)s: [test_client.py] [%(levelname)s] %(message)s')


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


def parse(response):
    if response:
        resp = response['response'][0]
        if 'error' in resp:
            print 'Error: ' + resp['error']['text'] + '. Code: ' + str(resp['error']['code'])
            logging.error(resp['error']['text'] + '. Code: ' + str(resp['error']['code']))
            return False
        else:
            return resp['params'][0]
    else:
        return False


def login_user(login, password, session_type, workstation_session_id):
    i = 0
    logging.info('Login: {0}. Password: {1}. Session type: {2}.'.format(login, password, session_type))
    info_user_session = user_auth(login, password, session_type)
    if info_user_session:
        print 'Successful login! \nSession ID: {0}.\nUser ID: {1}'. \
            format(info_user_session['session_id'], info_user_session['user_id'])
        logging.info('Successful login! Session ID: {0}. User ID: {1}'.
                     format(info_user_session['session_id'], info_user_session['user_id']))
        while i < 3:
            sleep(5)
            status = status_check(workstation_session_id)
            print status
            i += 1
        user_disconnect(info_user_session['session_id'], info_user_session['user_id'])


def main():
    i = 0
    need_continue = True
    login = 'jenko'
    password = hashlib.md5("oknej1984").hexdigest()
    session_type = 0
    while need_continue:
        info_station = workstation_auth()
        if info_station:
            info_station = Workstation(info_station)
            print 'Successful auth!\nWorkstation ID: {0}.\nWorkstation session ID: {1}.'. \
                format(info_station.workstation_id, info_station.workstation_session_id)
            logging.info('Successful auth! Workstation ID: {0}. Workstation session ID: {1}.'.
                         format(info_station.workstation_id, info_station.workstation_session_id))
            while i < 3:
                sleep(5)
                status = status_check(info_station.workstation_session_id)
                print status
                i += 1
            login_user(login, password, session_type, info_station.workstation_session_id)
            workstation_disconnect(info_station.workstation_session_id)
            need_continue = False
        else:
            sleep(10)

if __name__ == '__main__':
    main()