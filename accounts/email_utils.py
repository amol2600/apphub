import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException

from django.conf import settings


def send_brevo_email(
    subject,
    text_content,
    html_content,
    recipient_email,
):
    configuration = sib_api_v3_sdk.Configuration()

    configuration.api_key["api-key"] = settings.BREVO_API_KEY

    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
        sib_api_v3_sdk.ApiClient(configuration)
    )

    email = sib_api_v3_sdk.SendSmtpEmail(
        sender={
            "name": settings.BREVO_SENDER_NAME,
            "email": settings.BREVO_SENDER_EMAIL,
        },
        to=[
            {
                "email": recipient_email,
            }
        ],
        subject=subject,
        text_content=text_content,
    )

    if html_content:
        email.html_content = html_content

    try:
        api_instance.send_transac_email(email)

    except ApiException as e:
        print(e)
        raise