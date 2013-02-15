import ConfigParser
import socket
import mysqlhard
import os


def main():
    needs_param = ['AIDA64 Business Edition,Operating System,OS',
                 'Summary,Computer|Internet Explorer,IE',
                 'Summary,Computer|Date / Time,Time',
                 'Summary,Computer|Computer Name,CompName',
                 'Summary,Display|Video Adapter1,VideoAdapter',
                 'Summary,Motherboard|System Memory,RAM',
                 'Summary,Storage|Disk Drive1,HDD',
                 'Summary,Storage|SMART Hard Disks Status,SMART',
                 'Summary,Partitions|Partition1,DiskC',
                 'Summary,Partitions|Partition2,DiskD',
                 'Summary,Network|Primary IP Address,IP',
                 'Summary,Network|Primary MAC Address,MAC',
                 'Summary,DMI|DMI BIOS Version,BIOS_Ver',
                 'DMI,Motherboard|Motherboard Properties|Product,Motherboard',
                 'DMI,Processors1|Processor Properties|Version,Processor',
                 'Windows Video,Windows Video1|Video Adapter Properties|Driver Version,VideoDriver',
                 'Sensor,Temperatures|CPU,temp_proc',
                 'Sensor,Temperatures|GPU Diode (DispIO),temp_video',
                 'DMI,Memory Controller|Memory Controller Properties|Memory Slots,spd_count']
    config.read('C:/report.ini')
    for name in needs_param:
        i = name.split(',')
        print i[2] + ': ' + config.get(i[0], i[1])
        mysqlhard.insert_data(club, comp, i[2], config.get(i[0], i[1]))

    spd_count = int(config.get('DMI', 'Memory Controller|Memory Controller Properties|Memory Slots'))

    for i in range(1, spd_count + 1):
        name = 'SPD' + str(i)
        option = name + '|Memory Module Properties|Module Name'
        value = config.get('SPD', option)
        mysqlhard.insert_data(club, comp, name, value)
        print name + ': ' + value

    if os.path.exists('C:/version.txt'):
        file = open('C:/version.txt', 'r')
        version = file.read()
        print "Verison of image: " + version
        mysqlhard.insert_data(club, comp, 'img_ver', version)

if __name__ == '__main__':
    dict = {}
    ip = socket.gethostbyname(socket.gethostname())
    club = ip.split('.')[2]
    comp = ip.split('.')[3]
    config = ConfigParser.RawConfigParser()
    main()