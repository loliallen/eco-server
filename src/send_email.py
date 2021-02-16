from flask_mail import Mail, Message

mail = Mail()


def send_email(message: Message):
    mail.send(message)
