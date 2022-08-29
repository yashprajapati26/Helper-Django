

from django.core.mail import send_mail
from helper_project.settings import EMAIL_HOST_USER
from helper_project.celery import app

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




# def sendmail(subject,template,to,context):
#     subject = subject
#     template_str = template+'.html'
#     html_message = render_to_string(template_str, {'data': context})
#     plain_message = strip_tags(html_message)
#     from_email = 'projectPY2@gmail.com'
#     send_mail(subject, plain_message, from_email, [to], html_message=html_message)
