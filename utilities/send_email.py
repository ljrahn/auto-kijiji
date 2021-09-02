import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class SendEmail:
    def __init__(self, subject="rtl-soak results",
                 body="These are RTL soak results",
                 sender_email="lucasrahn09@gmail.com",
                 password='lucabut098890',
                 recipients=['lucasrahn09@gmail.com', 'rahnbryan@gmail.com', 'rahnjacob01@gmail.com', 'rahn_jacob@yahoo.ca']):
        self.subject = subject
        self.body = body
        self.sender_email = sender_email
        self.recipients = recipients
        self.password = password

    def send_email(self):
        # Create a multipart message and set headers
        message = MIMEMultipart()
        message["From"] = self.sender_email
        message['To'] = ", ".join(self.recipients)
        message["Subject"] = self.subject

        # Add body to email
        message.attach(MIMEText(self.body, "plain"))

        text = message.as_string()

        # Log in to server using secure context and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(self.sender_email, self.password)
            server.sendmail(self.sender_email, self.recipients, text)
