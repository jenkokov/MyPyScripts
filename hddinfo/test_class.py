__author__ = 'Jenko'




def main():


    testMap = { "my computer": Folder( 100, 50 ), "my documents": Folder( 150, 250 ) }
    print testMap['my computer'].size
    if 'my computer' in testMap:
        print 'ok!'

class Folder ():
    def __init__(self, size, region):
        self.size = size
        self.region = region

    def __repr__(self):
        return str(self.size) +','+str(self.region)






if __name__ == '__main__':
    main()


