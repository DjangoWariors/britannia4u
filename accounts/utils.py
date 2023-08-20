import json

import chardet
import pyotp
import requests
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage, message
from django.conf import settings

from django.core.exceptions import PermissionDenied

from accounts.models import SmsLog


# Restrict the vendor from accessing the customer page
def check_role_admin(user):
    if user.role == 'Admin':
        return True
    else:
        raise PermissionDenied


# Restrict the customer from accessing the vendor page
def check_role_customer(user):
    print(user.role)
    if user.role == 'Admin':
        return True
    else:
        raise PermissionDenied


def detectUser(user):
    print(user.role)
    print('praveen')
    if user.role == 'Admin':
        redirectUrl = 'admin-dashboard'
    elif user.role == 2:
        redirectUrl = 'panelist-Dashboard'
    elif user.role == None and user.is_superadmin:
        redirectUrl = '/admin'

    return redirectUrl


def send_verification_email(request, user, mail_subject, email_template):
    from_email = settings.DEFAULT_FROM_EMAIL
    current_site = get_current_site(request)
    message = render_to_string(email_template, {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    })
    to_email = user.email
    mail = EmailMessage(mail_subject, message, from_email, to=[to_email])
    mail.content_subtype = "html"
    mail.send()


def send_notification(mail_subject, mail_template, context):
    from_email = settings.DEFAULT_FROM_EMAIL
    message = render_to_string(mail_template, context)
    if (isinstance(context['to_email'], str)):
        to_email = []
        to_email.append(context['to_email'])
    else:
        to_email = context['to_email']
    mail = EmailMessage(mail_subject, message, from_email, to=to_email)
    mail.content_subtype = "html"
    mail.send()


def generate_otp_():
    base32_secret = pyotp.random_base32()
    totp = pyotp.TOTP(base32_secret)
    otp = totp.at(0)  # Generate OTP for the current time (time step = 0)
    return otp.zfill(6)


def generate_otp():
    base32_secret = pyotp.random_base32()
    totp = pyotp.TOTP(base32_secret)
    return totp.now()


def send_sms(mobile, msg, template):

    url = f"http://www.smsbox.in/api/sms/SendSMS.aspx?usr=Beyondmsolution&key=97D0CD38-1AA1-4227-8E33-4393EF7B4CCB" \
          f"&&smstype=TextSMS&to={mobile}&msg={msg}&rout=Transactional&from=CRZBRN&templateid={template}"
    response = requests.get(url)
    if response.status_code == 200:
        response_dict = json.loads(response.text)
        status = response_dict['status']
        #sms_log = SmsLog(user_id='', mobile=mobile, template=template, message=msg,status=status,api_response=response_dict)
        #sms_log.save()

def read_file_content(csv_file):
    # Read the file content and detect its encoding using chardet
    content = csv_file.read()
    encoding_info = chardet.detect(content)
    encoding = encoding_info['encoding']

    # Decode the content using the detected encoding
    try:
        decoded_content = content.decode(encoding)
        return decoded_content
    except UnicodeDecodeError:
        raise Exception("Failed to decode the file. Please ensure the file is in a valid encoding.")
