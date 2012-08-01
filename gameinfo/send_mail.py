"""
import smtplib

SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587

sender = 'jenko.kov@gmail.com'
recipient = 'jenko.kov@gmail.com'
subject = 'Gmail SMTP Test'
body = '''<table>


<tr>
<td colspan="2"></td>
</tr>


<tr>
<td></td>
<td></td>
</tr>


</table>'''

"Sends an e-mail to the specified recipient."

body = "" + body + ""

headers = ["From: " + sender,
           "Subject: " + subject,
           "To: " + recipient,
           "MIME-Version: 1.0",
           "Content-Type: text/html"]
headers = "\r\n".join(headers)

session = smtplib.SMTP(server, port)

session.ehlo()
session.starttls()
session.ehlo
session.login(sender, password)

session.sendmail(sender, recipient, headers + "\r\n\r\n" + body)
session.quit()
"""
import smtplib

def send_text_file(file, subject=file):
    usr='jenko.kov'
    psw='efi42dekut'
    fromaddr='jenko.kov@gmail.com'
    toaddr='jenko.kov@gmail.com'
    f = open(file,'rb')

    server=smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(usr,psw)

    # Send email
    m="From: %s\r\nTo: %s\r\nSubject: %s\r\nX-Mailer: My-Mail\r\n\r\n" % (fromaddr, toaddr, subject)
    text = f.read()
    server.sendmail(fromaddr, toaddr, m+text)
    server.quit()
    print '{0} send successful!'.format(file)
