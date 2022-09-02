

from django.core.mail import send_mail
from helper_project.settings import EMAIL_HOST_USER
from helper_project.celery import app
from .models import User

def send_otp_verification_mail(reciver,otp):
    subject = "Helper : Email Login OTP Verification"
    message = '''Hey User!
                         A sign in attempt requires further verification because we did not recognize your device. 
               To complete the sign in, enter the verification code on the unrecognized device.
               Verification code: ''' + otp 
    sender = EMAIL_HOST_USER
    reciver = reciver
    send_mail(subject,message,sender,[reciver])



def send_mail_to_vendor(reciver,message):
    subject = "Helper : Vendor confirmation"
    message = message
    sender = EMAIL_HOST_USER
    reciver = reciver
    send_mail(subject,message,sender,[reciver])




@app.task
def send_mail_for_contact(reciver,message):
    print("----------------------------")
    subject = "Helper : Conatct You Soon"
    message = message
    sender = EMAIL_HOST_USER
    reciver = reciver
    send_mail(subject,message,sender,[reciver])



@app.task   
def send_mail_by_admin():

    users = User.objects.all()

    for user in users:
        subject = "Hii !! Celery Testing"
        message = "If you are liking please must try celery in django"
        to = user.email
        from_email = EMAIL_HOST_USER
        send_mail(subject, message, from_email, [to])
