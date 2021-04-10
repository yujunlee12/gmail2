import smtplib
import mimetypes
import os
import chardet
from email.utils import formataddr
from email.header import Header
from email.message import Message
from email.mime.base import MIMEBase
from email.mime.audio import MIMEAudio
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
smtp_info={'gmail.com' : ('smtp.gmail.com',587)}

def send_email(sender_tup, receivers, subject, message, attach_files=(), passwd='',subtype='plain'):
    sender = formataddr(sender_tup)
    mail_to=[formataddr(rec) for rec in receivers]

    outer =MIMEBase('multipart','mixed')
    outer['Subject']=Header(subject.encode('utf-8'), 'utf')
    outer['From'] = sender
    outer['To'] =','.join(mail_to)
    outer.preamble = 'Hi\n'
    outer.epilogue =''
    msg = MIMEText(message.encode('utf-8'), _subtype=subtype, _charset='uft-8')
    outer.attach(msg)

    for fpath in attach_files:
        folder, file_name=os.path.split(fpath)
        ctype,_=mimetypes.guess_type(file_name)
        if ctype is None:
            ctype = 'application/octet-stream'
        maintype, subtype = ctype.split('/',1)
        with open(fpath, 'rb') as f:
            body = f.read()
        if maintype =='text':
            encoding = chardet.detect(body)['encoding']
            msg=MIMEText(body, _subtype=subtype, _charset=endoing)
        elif maintype =='image':
            msg =MIMEImage(body, _subtype=subtype)
        elif maintype =='audio':
            msg =MIMEAudio(body, _subtype=subtype)
        else:
            msg=MIMEApplication(body, _subtype=subtype)
        msg.add_header('Content-Disposition', 'attachment',filename=(Header(file_name, 'utf-8').encode()))
        outer.attach(msg)

        _, host = sender_tup[1].rsplit('@',1)
        smtp_server, port =smtp_info[host]

        if port== 587:
            smtp = smtplib.SMTP(smtp_server, port)
            rcode1, _ = smtp.ehlo()
            rcode2, _ =smtp.starttls()
        else:
            smtp=smtplib.SMTP_SSL(smtp_server, port)
            rcode1, _ = smtp.ehlo()
            rcode2 = 220

        if rcode1 != 250 or rcode2 !=220:
            smtp.quit()
            teturn('conection failed')


        smtp.login(sender_tup[1], passwd)
        smtp.sendmail(sender, mail_to, outer.as_string())
        smtp.quit()
            
        
    
