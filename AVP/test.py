import mysqlavp

for i in range(1, 100):
    check = mysqlavp.check_inbase(20, i)
    if check == 1:
        print 'Comp {0} exists'.format(i)
    else:
        print 'Comp {0} no exists'.format(i)
