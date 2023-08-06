import smtplib
     
class send_mail_mixin():
    def __init__(self):
        pass
        
    def send_mail(self, acct:str):
        sender = "efk-team@email.esunbank.com.tw"
        receivers = ['ang-19099@email.esunbank.com.tw']
        SUBJECT = "EFK account setup test"
        TEXT = f"Add new account: {acct}, it needs to change his/her password manually."
        message = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)
        try:
            with smtplib.SMTP("172.17.235.90", 25) as smtp:
                smtp.ehlo()
                status = smtp.sendmail(sender, receivers, message) 
        except:
            raise