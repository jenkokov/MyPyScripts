import zipfile
import os
import socket
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders

send_from = 'jenko@itland.net.ua'
comp_name = os.environ['COMPUTERNAME']
print comp_name


def send_mail(send_to, subject, text, file):

    msg = MIMEMultipart()
    msg['From'] = 'ITLand test comp ' + comp_name + ' <jenko@itland.net.ua>'
    msg['To'] = send_to
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(text))

    part = MIMEBase('application', "octet-stream")
    part.set_payload(open(file, "rb").read())
    Encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(file))
    msg.attach(part)

    server = smtplib.SMTP('172.16.10.254:25')
    server.sendmail(send_from, send_to, msg.as_string())
    server.quit()


def main(archive_list, zfilename='C:\\logs.zip'):
    print zfilename
    z_out = zipfile.ZipFile(zfilename, "w", zipfile.ZIP_DEFLATED)
    for fname in archive_list:
        print "Compressing: ", fname
        z_out.write('C:\\dslogon\\' + fname)
    z_out.close()

if __name__ == '__main__':
    ip = socket.gethostbyname(socket.gethostname())
    archive_list = os.listdir('C:\\dslogon\\')
    main(archive_list)
    text = raw_input('Enter text to send in mail: ')
    print 'Sending mail to kolesnichenko@gmail.com...'
    send_mail('kolesnichenko@gmail.com', 'logs from {0}'.format(ip), text, 'C:\\logs.zip')
    print 'Mail sent.'
    raw_input('Press \'Enter\' to exit')