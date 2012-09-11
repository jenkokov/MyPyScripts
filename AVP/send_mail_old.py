import smtplib

def send_text_file(file, subject=file):
    usr='jenko.kov'
    psw='efi42dekut'
    fromaddr='jenko.kov@gmail.com'
    toaddr='jenko.kov@gmail.com'
    f = open(file,'r')

    server=smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(usr,psw)

    # Send email
    m="From: %s\r\nTo: %s\r\nSubject: %s\r\nX-Mailer: My-Mail\r\n\r\n" % (fromaddr, toaddr, subject)
    text = f.read()
    server.sendmail(fromaddr, toaddr, m+text)
    server.quit()
    print '{0} send successful!'.format(file)


