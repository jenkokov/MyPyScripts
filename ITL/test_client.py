import os
import hashlib
from random import choice
from server_operation import *
from time import sleep
from random import randint
import mysqlitl
import socket


general_log = 'C:\\dslogon\\general.log'
if not os.path.exists('C:\\dslogon\\'):
    os.makedirs('C:\\dslogon\\')
    f = open(general_log, 'a')
    f.close()

settings = mysqlitl.get_settings()
cooldown = float(settings['cooldown'])
warn_time = float(settings['warn_time'])
infinite = int(settings['infinite'])

ip = socket.gethostbyname(socket.gethostname())
club = ip.split('.')[2]
comp = ip.split('.')[3]


def print_log(level, operation, string, time=0):
    if time > warn_time:
        level = 'Over time'
        mysqlitl.insert_warning(comp, operation, time)
    f = open(general_log, 'a')
    if time != 0:
        data = '[{0}] [{1}] [{2}] {3}'.format(level.upper(), str(time)[:8], operation, string)
    else:
        data = '[{0}] {1}'.format(level.upper(), string)
    f.write(data + '\n')
    print data
    f.close()


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
            print_log('error', 'parser', 'Error: ' + resp['error']['text'] + '. Code: ' + str(resp['error']['code']))
            return False
        else:
            if len(resp['params']) == 1:
                return resp['params'][0]
            else:
                return resp['params']
    else:
        return False


def get_content_id_dict(session_id, user_id):
    id_dict = []
    response = content_list(session_id, user_id)
    time = response[1]
    print_log('info', 'content_list', 'Get content list', time)
    if response[0]:
        resp = response[0]['response'][0]
        if 'error' in resp:
            print_log('error', 'parser', 'Error: ' + resp['error']['text'] + '. Code: ' + str(resp['error']['code']))
            return False
        else:
            for game in resp['params']:
                id_dict.append(game['dic_content_id'])
            return id_dict
    else:
        return False


def launch_content(session_id, user_id, workstation_session_id):
    content_id = choice(get_content_id_dict(session_id, user_id))
    dic_content_action_id = application_action(session_id, user_id, 'start', content_id)
    time = dic_content_action_id[1]
    dic_content_action_id = dic_content_action_id[0]['dic_content_action_id']
    if dic_content_action_id:
        i = 0
        print_log('info', 'application_action', 'Successful launch content with ID {1}. dic_content_action_id: {0}'.format(dic_content_action_id, content_id), time)
        while i < randint(2, 5):
            sleep(cooldown)
            status = status_check(workstation_session_id)
            print_log('info', 'status_check', status[0], status[1])
            i += 1
        sleep(cooldown)
        time = application_action(session_id, user_id, 'stop', dic_content_action_id)[1]
        print_log('info', 'application_action', 'Closing content with dic_content_action_id {0}.'.format(dic_content_action_id), time)
        return True
    else:
        return False


def login_user(login, password, session_type, workstation_session_id):
    i, a = 0, 0
    info_user_session = user_auth(login, password, session_type)
    if info_user_session[0]:
        session_id = info_user_session[0]['session_id']
        user_id = info_user_session[0]['user_id']
        print_log('info', 'user_auth', 'Successful login. Session ID: {0}. User ID: {1}'.format(session_id, user_id), info_user_session[1])
        while i < randint(2, 10):
            sleep(cooldown)
            status = status_check(workstation_session_id)
            print_log('info', 'status_check', status[0], status[1])
            i += 1
        while a < randint(2, 10):
            try:
                launch_content(session_id, user_id, workstation_session_id)
            except:
                pass
            a += 1
        data = user_disconnect(session_id, user_id)
        print_log('info', 'user_disconnect', 'Disconnect user with ID {0}'.format(user_id), data[1])


def main():
    need_continue = True
    #login = 'jenko'
    #password = hashlib.md5("oknej1984").hexdigest()
    session_type = 0
    while need_continue:
        info_station = workstation_auth()
        if info_station[0]:
            time = info_station[1]
            info_station = Workstation(info_station[0])
            print_log('info', 'workstation_auth', 'Successful auth! Workstation ID: {0}. Workstation session ID: {1}.'
                      .format(info_station.workstation_id, info_station.workstation_session_id), time)
            i = 0
            while i < randint(2, 10):
                user = get_user()
                login = user['login']
                password = user['pass']
                if not password:
                    continue
                sleep(cooldown)
                status = status_check(info_station.workstation_session_id)
                print_log('info', 'status_check', status[0], status[1])
                i += 1
                login_user(login, password, session_type, info_station.workstation_session_id)
            data = workstation_disconnect(info_station.workstation_session_id)
            print_log('info', 'workstation_disconnect', 'Disconnect workstation with session ID {0}'.format(info_station.workstation_session_id), data[1])
            sleep(cooldown * 3)
            if infinite == 0:
                need_continue = False
            else:
                need_continue = True
        else:
            sleep(cooldown * 2)
if __name__ == '__main__':
    main()