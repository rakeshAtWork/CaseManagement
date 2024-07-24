import random
from rest_framework.pagination import PageNumberPagination
from decouple import config
from datetime import datetime, timedelta
import jwt
import base64
from django.conf import settings

from django.core.mail import EmailMultiAlternatives
from django.conf import settings


def decode_base64(base64_bytes):
    try:
        decoded_data = base64.b64decode(base64_bytes)
        return decoded_data
    except:
        return None


def generate_token(user_email):
    """Generate JWT token."""
    payload = {
        'email': user_email,
        'exp': datetime.utcnow() + timedelta(minutes=int(config("TOKEN_TTL"))),
        'iat': datetime.utcnow(),
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256').decode('utf-8')


def decode_token(token):
    """Decode and verify JWT token."""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        return payload.get('email')
    except jwt.ExpiredSignatureError:
        # Token has expired
        return None
    except jwt.InvalidTokenError:
        # Token is invalid
        return None
    except Exception:
        return None


def get_random_string(length=12, allowed_chars='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'):
    """
    Return a  generated random string.
    """

    return ''.join(random.choice(allowed_chars) for _ in range(length))


class CustomPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 10000


def new_user_registration_msg(user):
    msg = f"Dear {user.first_name} {user.last_name}\n\n" \
          f" You have been successfully register in Case Management System.you can login after" \
          f" the approval from the admin. "
    return msg


def account_activate_new_password_msg(user, new_password):
    msg = f"Dear {user.first_name} {user.last_name}, Your account has been activated.\n\n" \
          f"We have changed your password. Please login with your new credentials.\n\n" \
          f"Email: {user.email}\n" \
          f"Password: {new_password}\n\n" \
          f"Regards,\n" \
          f"Case Management System"
    return msg


def send_html_email(to_email, subject, html_content):
    """
    Send an HTML email to a particular user.

    :param to_email: Recipient's email address
    :param subject: Subject of the email
    :param html_content: HTML content of the email
    """
    from_email = settings.EMAIL_HOST_USER
    text_content = 'This is an important message.'  # Optional plain text content

    # Create the email message
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    msg.attach_alternative(html_content, "text/html")

    # Send the email
    msg.send()


def email_send(user_mail, subject, message):
    email_content = """
        <!DOCTYPE><html><head><title>Cozentus</title><meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
        <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
        <style type="text/css">a{outline:none;color:#40aceb;text-decoration:underline;}a:hover{text-decoration:none !important;}.nav a:hover{text-decoration:underline !important;}.title a:hover{text-decoration:underline !important;}.title-2 a:hover{text-decoration:underline !important;}.btn:hover{opacity:0.8;}.btn a:hover{text-decoration:none !important;}.btn{-webkit-transition:all 0.3s ease;-moz-transition:all 0.3s ease;-ms-transition:all 0.3s ease;transition:all 0.3s ease;}table td{border-collapse: collapse !important;}.ExternalClass, .ExternalClass a, .ExternalClass span, .ExternalClass b, .ExternalClass br, .ExternalClass p, .ExternalClass div{line-height:inherit;}@media only screen and (max-width:500px){table[class="flexible"]{width:100% !important;}table[class="center"]{float:none !important;margin:0 auto !important;}*[class="hide"]{display:none !important;width:0 !important;height:0 !important;padding:0 !important;font-size:0 !important;line-height:0 !important;}td[class="img-flex"] img{width:100% !important;height:auto !important;}td[class="aligncenter"]{text-align:center !important;}th[class="flex"]{display:block !important;width:100% !important;}td[class="wrapper"]{padding:0 !important;}td[class="holder"]{padding:30px 15px 20px !important;}td[class="nav"]{padding:20px 0 0 !important;text-align:center !important;}td[class="h-auto"]{height:auto !important;}td[class="description"]{padding:30px 20px !important;}td[class="i-120"] img{width:120px !important;height:auto !important;}td[class="footer"]{padding:5px 20px 20px !important;}td[class="footer"] td[class="aligncenter"]{line-height:25px !important;padding:20px 0 0 !important;}tr[class="table-holder"]{display:table !important;width:100% !important;}th[class="thead"]{display:table-header-group !important; width:100% !important;}th[class="tfoot"]{display:table-footer-group !important; width:100% !important;}}</style></head>
        <body style="margin:0; padding:0;" bgcolor="#eaeced">
        <table style="min-width:320px;" width="100%" cellspacing="0" cellpadding="0" bgcolor="#eaeced">
        <tr>
        <td class="hide">
            <table width="600" cellpadding="0" cellspacing="0" style="width:600px !important;">
            <tr>
            <td style="min-width:600px; font-size:0; line-height:0;">&nbsp;</td>
            </tr>
            </table>
        </td>
        </tr>
        <tr>
        <td class="wrapper" style="padding:0 10px;">
        <table data-module="module-1" data-thumb="thumbnails/01.png" width="100%" cellpadding="0" cellspacing="0">
        <tr>
        <td data-bgcolor="bg-module" bgcolor="#eaeced">
        <table class="flexible" width="600" align="center" style="margin:0 auto;" cellpadding="0" cellspacing="0">
        <tr><td style="padding:29px 0 30px;">
        <table width="100%" cellpadding="0" cellspacing="0">
        <tr><th class="flex" width="113" align="left" style="padding:0;">
        <table class="center" cellpadding="0" cellspacing="0"><tr><td style="line-height:0;">
        <a target="_blank" style="text-decoration:none;" href="http://portal.cozentus.com/">
        <img src="https://images.squarespace-cdn.com/content/v1/61013e1f8b0c8e0cd83e6fb5/8d6b05a5-c0d5-4644-a36b-706b6e4fc52c/logo+png+%281%29.png?format=1500w" border="0" style="font:bold 12px/12px Arial, Helvetica, sans-serif; color:#606060;" align="left" vspace="0" hspace="0" width="100%" alt="COZENTUS"/>
        </a></td></tr></table></th>
        <th class="flex" align="left" style="padding:0;"><table width="100%" cellpadding="0" cellspacing="0"><tr><td data-color="text" data-size="size navigation" data-min="10" data-max="22" data-link-style="text-decoration:none; color:#888;" class="nav" align="right" style="font:bold 13px/15px Arial, Helvetica, sans-serif; color:#888;">
        <a target="_blank" style="text-decoration:none; color:#888;" href="http://portal.cozentus.com/">Home</a>&nbsp; &nbsp; <a target="_blank" style="text-decoration:none; color:#888;" href="http://portal.cozentus.com/">Contact</a></td>
        </tr></table></th></tr></table></td></tr></table></td></tr>
        </table><table data-module="module-2" data-thumb="thumbnails/02.png" width="100%" cellpadding="0" cellspacing="0">
        <tr><td data-bgcolor="bg-module" bgcolor="#eaeced"><table class="flexible" width="600" align="center" style="margin:0 auto;" cellpadding="0" cellspacing="0">
        <tr><td data-bgcolor="bg-block" class="holder" style="padding:58px 60px 52px;" bgcolor="#f9f9f9">
        <table width="100%" cellpadding="0" cellspacing="0"><tr><td data-color="title" data-size="size title" data-min="25" data-max="45" data-link-color="link title color" data-link-style="text-decoration:none; color:#292c34;" class="title" align="center" style="font:35px/38px Arial, Helvetica, sans-serif; color:#292c34; padding:0 0 24px;">""" + subject + """</td></tr><tr><td data-color="text" data-size="size text" data-min="10" data-max="26" data-link-color="link text color" data-link-style="font-weight:bold; text-decoration:underline; color:#40aceb;" align="center" style="font:bold 16px/25px Arial, Helvetica, sans-serif; color:#888; padding:0 0 23px;">""" \
                    + message \
                    + """</td></tr></table></td></tr><tr><td height="28"></td></tr></table></td></tr>
                    </table><table data-module="module-7" data-thumb="thumbnails/07.png" width="100%" cellpadding="0" cellspacing="0"><tr><td data-bgcolor="bg-module" bgcolor="#eaeced"><table class="flexible" width="600" align="center" style="margin:0 auto;" cellpadding="0" cellspacing="0"><tr><td class="footer" style="padding:0 0 10px;"><table width="100%" cellpadding="0" cellspacing="0"><tr class="table-holder"><th class="tfoot" width="400" align="left" style="vertical-align:top; padding:0;">
                    <table width="100%" cellpadding="0" cellspacing="0"><tr><td data-color="text" data-link-color="link text color" data-link-style="text-decoration:underline; color:#797c82;" class="aligncenter" style="font:12px/16px Arial, Helvetica, sans-serif; color:#797c82; padding:0 0 10px;">Cozentus Private Limited, 2022. &nbsp; All Rights Reserved. <a target="_blank" style="text-decoration:underline; color:#797c82;">Please Do Not Reply.</a></td></tr></table>
                    </th></tr></table></td></tr></table></td></tr></table></td></tr><tr><td style="line-height:0;"><div style="display:none; white-space:nowrap; font:15px/1px courier;">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;</div></td></tr></table></body></html>"""
    send_html_email(user_mail, subject, email_content)
