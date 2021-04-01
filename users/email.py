from templated_mail.mail import BaseEmailMessage
from djoser.email import (
    ActivationEmail,
    PasswordResetEmail
)


class CustomActivationEmail(ActivationEmail):
    template_name = 'email/activation.html'


class CustomPasswordResetEmail(PasswordResetEmail):
    template_name = 'email/password_reset.html'


class InformingEmail(BaseEmailMessage):
    template_name = "email/informing.html"


class ReceiveRequestEmail(BaseEmailMessage):
    template_name = "email/receive_request.html"


class ResponseRequestEmail(BaseEmailMessage):
    template_name = "email/response_request.html"
