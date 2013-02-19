import mysqlhard

for i in range(1, 100):
    check = mysqlhard.check_in_base(20, i)
    if check == 1:
        print 'Comp {0} exists'.format(i)
    else:
        print 'Comp {0} no exists'.format(i)
