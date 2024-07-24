import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from decouple import config


def send_mail(SUBJECT, BODY, TO):
    """With this function we send out our html email"""

    # Create message container - the correct MIME type is multipart/alternative here!
    FROM=config("EMAIL_HOST_USER")
    MESSAGE = MIMEMultipart('alternative')
    MESSAGE['subject'] = SUBJECT
    recipient=TO if isinstance(TO, list) else [TO]
    MESSAGE['To'] = TO
    MESSAGE['From'] = FROM
    MESSAGE.preamble = """
Your mail reader does not support the report format.
Please visit us <a href="http://things.epsumlabs.com">online</a>!"""

    # Record the MIME type text/html.
    HTML_BODY = MIMEText(BODY, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    MESSAGE.attach(HTML_BODY)

    # The actual sending of the e-mail
    server = smtplib.SMTP(host=config("EMAIL_HOST"),port=int(config("EMAIL_PORT")))


    # Print debugging output when testing
    if __name__ == "__main__":
        server.set_debuglevel(1)

    # Credentials (if needed) for sending the mail
    password = config("EMAIL_HOST_PASSWORD")

    server.starttls()
    server.login(FROM, password)
    server.sendmail(FROM, TO, MESSAGE.as_string())
    server.quit()


