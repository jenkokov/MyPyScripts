import ConfigParser
import socket
import mysqlhard


def main():
    needs_param=['AIDA64 Business Edition,Operating System,OS',
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
                 'Windows Video,Windows Video1|Video Adapter Properties|Driver Version,VideoDriver'
                ]
    config.read('C:/report.ini')
    section_list = ConfigParser.RawConfigParser.sections(config)
    for name in needs_param:
        i=name.split(',')
        print i[2]+': '+config.get(i[0],i[1])
        mysqlhard.insert_data(club,comp,i[2],config.get(i[0],i[1]))
if __name__ == '__main__':
    dict = {}
    ip = socket.gethostbyname(socket.gethostname())
    club = ip.split('.')[2]
    comp = ip.split('.')[3]
    config = ConfigParser.RawConfigParser()
    main()