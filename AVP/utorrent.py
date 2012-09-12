import sys

def main():
    print 'Torrent: '+sys.argv[1]
    print 'Status: '+status_dict[sys.argv[2]]
    raw_input('Pause')


if __name__=='__main__':
    status_dict={'1':'Error!', '2':'Checking', '3': 'Pause','4':'SuperSeed','5':'Seeding',
       '6':'Downloading','7':'SuperSeed[F]','8':'Seeding[F]','9':'Downloading[F]','10':'Wait seeding',
       '11':'Complete','12':'In queue','13':'Stopped'}
    main()