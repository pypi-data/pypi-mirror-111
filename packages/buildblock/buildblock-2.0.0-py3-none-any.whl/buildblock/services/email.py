import logging

from django.conf import settings
from django.core.mail import EmailMessage
from django.db.models import Q
from django.template.defaultfilters import linebreaks
from django.template.loader import get_template, render_to_string
from django.utils.translation import ugettext_lazy as _

from buildblock.apps.core.constants import COMMENT_ADD, COMMENT_DELETE, CREATED, STATUS_CHANGE
from buildblock.apps.users.models import User

logger = logging.getLogger(__name__)


class EmailService:
    def __send_mail(subject, message, email):
        try:
            mail = EmailMessage(subject, message, settings.DEFAULT_FROM_EMAIL, [email])
            mail.content_subtype = "html"  # Main content is now text/html
            mail.send()
            return True
        except Exception as e:
            logger.error(f'Sending Email failed: ' + e)
            return False

    def __send_mail_with_attach(subject, message, email, attach_list):
        try:
            mail = EmailMessage(subject, message, settings.DEFAULT_FROM_EMAIL, [email])
            mail.content_subtype = "html"  # Main content is now text/html

            for attach in attach_list:
                mail.attach(attach.name, attach.read(), attach.content_type)
            mail.send()
            return True
        except Exception as e:
            logger.error(f'Sending Email failed: ' + e)
            return False

    @classmethod
    def check_template_exists(cls, form_name):
        try:
            get_template(f'email/{form_name}.html')
        except Exception:
            return False
        else:
            return True

    # TODO should make this method more general cases
    @classmethod
    def send_to_admin(cls, name, email):
        subject = "[Notification] Landing Page Subscription"

        message = f"""
        Name: {name}<br>
        E-mail: {email}<br>
        """
        result = cls.__send_mail(subject, message, settings.DEFAULT_FROM_EMAIL)
        logger.info(f'Email has successfully been sent to the admin: {name} {email}')
        return result

    # 한 입금 확인 알림 메일 발송
    @classmethod
    def send_deposit_verified_to_user(cls, name, email, bb_amount):
        # bb_amount: 빌드블록에서 충전해준 BBT 금액. 이더리움 한화 동시 사용
        email_data = {
            "user_name": name,
            "user_email": email,
            "bb_amount": bb_amount,
        }
        subject = _("[빌드블록] 입금 확인 및 충전 완료 알림")
        message = render_to_string('email/trade_charge_success.html', email_data)

        result = cls.__send_mail(subject, message, email)
        logger.info('User has successfully been notified about the verified deposit - ' +
                    f'email: {email}, amount: {bb_amount}')
        return result

    @classmethod
    def send_to_admin_exit_request(cls, name, email):
        subject = "[알림] 회원탈퇴 신청자가 있습니다."

        message = f"""
        이름: {name}<br>
        이메일: {email}<br>
        """

        result = cls.__send_mail(subject, message, settings.DEFAULT_FROM_EMAIL)
        logger.info(f'Email has successfully been sent to the admin: {name} {email}')
        return result

    @classmethod
    def send_to_admin_contact_us(cls, name, email, content):
        subject = "[알림] 문의 사항이 접수되었습니다."
        content = linebreaks(content)

        message = f"""
        이름: {name}<br>
        이메일: {email}<br>
        <br>
        {content}
        """

        result = cls.__send_mail(subject, message, settings.DEFAULT_FROM_EMAIL)
        logger.info(f'Email has successfully been sent to the admin: {name} {email}')
        return result

    # 페이팔 결제 오류 알림 메일
    @classmethod
    def send_paypal_error_alert_to_admin(cls, email, orderId):
        subject = "[알림] Paypal 결제 과정에서 문제가 발생했습니다."
        message = f"""
        Email: {email}<br>
        OrderID: {orderId}<br>
        Paypal Dashboard 와 어드민 페이지 MoneyTransaction 테이블을 확인해주세요
        """
        result = cls.__send_mail(subject, message, settings.DEFAULT_FROM_EMAIL)
        return result

    @classmethod
    def send_maintenance_request_created(cls, email_data):
        subject = "[Notification] Your maintenance request has been created."
        message = render_to_string('email/maintenance_created.html', email_data)
        result = cls.__send_mail(subject, message, email_data["user_email"])
        logger.info(f"Maintenance request for {email_data.get('user_name')} has been created.")
        return result

    @classmethod
    def send_maintenance_request_replied(cls, email_data):
        subject = "[Notification] Your maintenance request has been replied."
        message = render_to_string('email/maintenance_replied.html', email_data)
        result = cls.__send_mail(subject, message, email_data["user_email"])
        logger.info(f"Maintenance request for {email_data.get('user_name')} has been replied.")
        return result

    @classmethod
    def send_maintenance_comment_deleted(cls, email_data):
        subject = "[Notification] A comment was deleted from your maintenance request."
        message = render_to_string('email/maintenance_comment_deleted.html', email_data)
        result = cls.__send_mail(subject, message, email_data["user_email"])
        logger.info(f"A comment from a maintenance request for {email_data.get('user_name')} has been deleted.")
        return result

    @classmethod
    def send_maintenance_request_status_change(cls, email_data):
        subject = "[Notification] Status of your maintenance request has been changed."
        message = render_to_string('email/maintenance_status_change.html', email_data)
        result = cls.__send_mail(subject, message, email_data["user_email"])
        logger.info(f"Status of maintenance request for {email_data.get('user_name')} has been changed.")
        return result

    @classmethod
    def _send_emails_for_maintenace_event_type(cls, maintenance, request_user, event_type, comment=None):
        # Get Email Function
        execution_fn = {
            CREATED: cls.send_maintenance_request_created,
            STATUS_CHANGE: cls.send_maintenance_request_status_change,
            COMMENT_ADD:  cls.send_maintenance_request_replied,
            COMMENT_DELETE: cls.send_maintenance_comment_deleted,
        }.get(event_type)

        if not execution_fn:
            return

        # Owners & Agent (Exclude Writer)
        receivers = User.objects.filter(
            Q(owned_products=maintenance.product) | Q(groups=maintenance.product.agency)
        )
        receiver_dict = {
            receiver.email: receiver.name
            for receiver in receivers
        }
        if maintenance.tenant.email not in receiver_dict.keys():
            receiver_dict[maintenance.tenant.email] = maintenance.tenant.name
        if request_user.email in receiver_dict.keys():
            del receiver_dict[request_user.email]

        # Contents
        email_contents = {
            'product': maintenance.product.full_address,
            'maintenance_title': maintenance.title,
            'maintenance_status': maintenance.status,
            'maintenance_writer': maintenance.tenant.name,
            'request_user': request_user.name,
            'comment': comment,
        }

        for email, name in receiver_dict.items():
            email_data = {'user_name': name, 'user_email': email, 'contents': email_contents}
            execution_fn(email_data=email_data)

    @classmethod
    def send_investment_step_email(cls, email_data):
        subject = _("[Notification] Investment progress has been updated.")
        message = render_to_string('email/investment_step.html', email_data)
        result = cls.__send_mail(subject, message, email_data.get("user_email"))
        if result:
            logger.info(f"Investment Step Update email sent. - {email_data.get('user_name')}")
        if cls.__send_mail(subject, message, settings.DEFAULT_FROM_EMAIL):
            logger.info(f"Investment Step Update email sent. - {settings.DEFAULT_FROM_EMAIL}")
        return result

    @classmethod
    def send_admin_email_to_group(cls, recipients, title, message):
        email_data = {
            'title': title,
            'message': message,
        }
        subject = _(f"[BuildBlock] {title}")
        message = render_to_string('email/admin_email.html', email_data)

        for recipient in recipients:
            result = cls.__send_mail(subject, message, recipient)
            if not result:
                logger.info(f'Failed to send email to {recipient}')
                continue

        return result

    # landing page invest request
    @classmethod
    def send_to_admin_inquiry(cls, name, email, phone, survey, content):
        subject = "[알림] 투자 문의가 접수되었습니다."
        content = linebreaks(content)

        message = f"""
        이름 : {name}<br>
        이메일 : {email}<br>
        전화번호 : {phone}<br><br>
        <b>{survey}</b>
        <br><br>
        {content}
        """

        result = cls.__send_mail(subject, message, settings.DEFAULT_FROM_EMAIL)
        logger.info(f'Email has successfully been sent to the admin: {email} {phone}')
        return result

    @classmethod
    def send_property_list_email(cls, property_list, filter):
        subject = _("[Subscription] Property List: " + filter.title)
        email_data = {
            'property_list': property_list,
            'filter': filter,
        }
        message = render_to_string('email/property_sale_list.html', email_data)
        for email in filter.emails:
            cls.__send_mail(subject, message, email)

    @classmethod
    def send_contact_email_to_help(cls, name, email, phone, content):
        subject = "[알림] 홈페이지 문의가 접수되었습니다."
        content = linebreaks(content)

        message = f"""
        이름 : {name}<br>
        이메일 : {email}<br>
        전화번호 : {phone}<br><br>
        {content}
        """

        result = cls.__send_mail(subject, message, settings.DEFAULT_FROM_HELP_EMAIL)
        logger.info(f'Email has successfully been sent to the admin: {email} {phone}')
        return result
