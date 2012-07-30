import mysqlwork
import socket
import os


ip = socket.gethostbyname(socket.gethostname())
club = ip.split('.')[2]
comp = ip.split('.')[3]

print os.path.exists('D:/Games/AAAAA')