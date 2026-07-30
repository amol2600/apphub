from django.contrib.auth.forms import PasswordResetForm
from django.template.loader import render_to_string

from .email_utils import send_brevo_email


class BrevoPasswordResetForm(PasswordResetForm):

    def send_mail(
        self,
        subject_template_name,
        email_template_name,
        context,
        from_email,
        to_email,
        html_email_template_name=None,
    ):

        subject = render_to_string(
            subject_template_name,
            context,
        ).strip()

        text_content = render_to_string(
            email_template_name,
            context,
        )

        html_content = ""

        if html_email_template_name:

            html_content = render_to_string(
                html_email_template_name,
                context,
            )

        send_brevo_email(
            subject=subject,
            text_content=text_content,
            html_content=html_content,
            recipient_email=to_email,
        )