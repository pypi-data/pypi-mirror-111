import logging
from typing import Dict

from django.conf import settings
from django.core.mail import EmailMessage
from django.template import Context, Template
from django.urls import reverse

from buildblock.apps.core.constants import PAYMENT_REPORT, PAYMENT_REQUEST
from buildblock.apps.messaging.models import MessagingRequests, MessagingTemplates
from buildblock.apps.signed_url.handler import SignedUrlHandler
from buildblock.apps.users.models import User
from buildblock.helper import db_update
from buildblock.services.aws import AwsService

logger = logging.getLogger(__name__)


class MessagingService:
    @classmethod
    def get_messaging_template(cls, id):
        return MessagingTemplates.objects.get(id=id)

    @classmethod
    def render_content_by_messaging_template_id(cls, id, email_data):
        template_file = AwsService.get_messaging_template(id)
        return Template(template_file).render(Context(email_data))

    @classmethod
    def add_messaging_template(cls, creator_id, title, category, is_active, description):
        creator = User.objects.get(id=creator_id)
        return MessagingTemplates.objects.create(
            creator=creator,
            title=title,
            category=category,
            is_active=is_active,
            description=description
        )

    @classmethod
    def edit_messaging_template(cls, template_id, title, category, is_active, description):
        template = cls.get_messaging_template(template_id)
        db_update(template, dict(
            title=title,
            category=category,
            is_active=is_active,
            description=description,
        ))

    @staticmethod
    def send_message(title, content, receiver_emails: list, sender_email=settings.DEFAULT_FROM_EMAIL):
        try:
            mail = EmailMessage(title, content, sender_email, receiver_emails)
            mail.content_subtype = "html"
            mail.send()
            return True
        except Exception as e:
            logger.error(f'Sending Email failed: ' + e)
            return False

    @classmethod
    def send_message_with_template(cls, template_id, receiver_emails: list, email_data: Dict = None, email_title=None):
        messaging_template = cls.get_messaging_template(template_id)
        email_title = email_title or messaging_template.title
        content = cls.render_content_by_messaging_template_id(template_id, email_data)
        return cls.send_message(email_title, content, receiver_emails)

    @staticmethod
    def _create_messaging_request(title, content, receiver_emails: list, sender_email=settings.DEFAULT_FROM_EMAIL):
        return MessagingRequests.objects.create(
            title=title,
            content=content,
            sender=sender_email,
            receivers=receiver_emails
        )

    @classmethod
    def create_messaging_request_with_template(
        cls, template_id, receiver_emails: list, email_data: Dict = None, email_title=None
    ):
        messaging_template = cls.get_messaging_template(template_id)
        email_title = email_title or messaging_template.title
        content = cls.render_content_by_messaging_template_id(template_id, email_data)
        return cls._create_messaging_request(email_title, content, receiver_emails)

    @staticmethod
    def get_messaging_request_standby_list():
        return MessagingRequests.objects.filter(sent_at__isnull=True).order_by('created_at')

    @classmethod
    def send_property_list_email(cls, property_list, filter):
        if not filter.messaging_template:
            logger.error("The messaging template for the property email subscription does not exist.")
            return
        email_title = "[Subscription] Property List: " + filter.title
        for email in filter.emails:
            email_data = {
                'property_list': property_list,
                'filter': filter,
                'receiver_email': email
            }
            cls.send_message_with_template(
                template_id=filter.messaging_template.id,
                receiver_emails=[email],
                email_data=email_data,
                email_title=email_title,
            )

    @classmethod
    def schedule_payment_request_email(cls, payment_list, tenant):
        messaging_template = MessagingTemplates.objects.filter(
            category=PAYMENT_REQUEST,
            is_active=True
        ).last()
        if not messaging_template:
            logger.error("The messaging template for the payment request email does not exist.")
            return
        signed_url = SignedUrlHandler.create_signed_url(
            user_email=tenant.email,
            redirect_url=reverse('management:house'),
            expiration_days=7,
        )
        email_data = {
            'payment_list': payment_list,
            'tenant': tenant,
            'signed_url': signed_url,
        }
        cls.create_messaging_request_with_template(
            template_id=messaging_template.id,
            receiver_emails=[tenant.email],
            email_data=email_data,
            email_title="[Notification] Your rent is due.",
        )

    @classmethod
    def schedule_payment_report_email(cls, payment_data, agency):
        messaging_template = MessagingTemplates.objects.filter(
            category=PAYMENT_REPORT,
            is_active=True
        ).last()
        if not messaging_template:
            logger.error("The messaging template for the payment report email does not exist.")
            return
        receiver_emails = agency.user_set.values_list('email', flat=True)
        for receiver_email in receiver_emails:
            signed_url = SignedUrlHandler.create_signed_url(
                user_email=receiver_email,
                redirect_url=reverse('management:transaction'),
                expiration_days=7,
            )
            email_data = {
                'payment_data': payment_data,
                'agency': agency,
                'signed_url': signed_url,
            }
            cls.create_messaging_request_with_template(
                template_id=messaging_template.id,
                receiver_emails=[receiver_email],
                email_data=email_data,
                email_title="[Notification] Rent Payment Report",
            )
