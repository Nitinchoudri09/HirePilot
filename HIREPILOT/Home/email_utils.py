import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def send_brevo_email(to_email, to_name, subject, html_content):
    api_key = settings.BREVO_API_KEY
    sender_email = settings.BREVO_SENDER_EMAIL

    # Log what values are actually being used
    logger.error(f"[BREVO DEBUG] API key present: {bool(api_key)}, length: {len(api_key)}")
    logger.error(f"[BREVO DEBUG] Sender email: '{sender_email}'")
    logger.error(f"[BREVO DEBUG] Sending to: '{to_email}' name: '{to_name}'")
    logger.error(f"[BREVO DEBUG] Subject: '{subject}'")

    if not api_key:
        logger.error("[BREVO DEBUG] FATAL: BREVO_API_KEY is empty — check Render environment variables")
        return False

    if not sender_email:
        logger.error("[BREVO DEBUG] FATAL: BREVO_SENDER_EMAIL is empty — check Render environment variables")
        return False

    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = api_key

    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
        sib_api_v3_sdk.ApiClient(configuration)
    )

    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=[{"email": to_email, "name": to_name}],
        sender={"name": "HirePilot", "email": sender_email},
        subject=subject,
        html_content=html_content
    )

    try:
        response = api_instance.send_transac_email(send_smtp_email)
        logger.error(f"[BREVO DEBUG] SUCCESS — message ID: {response.message_id}")
        return True
    except ApiException as e:
        logger.error(f"[BREVO DEBUG] ApiException status={e.status} reason={e.reason} body={e.body}")
        return False
    except Exception as e:
        logger.error(f"[BREVO DEBUG] Unexpected error: {type(e).__name__}: {e}")
        return False
