import logging
from datetime import date, datetime, timedelta

import pytz
from background_task import background
from background_task.models import Task
from dateutil.relativedelta import relativedelta
from django.db.models import Q
from django.utils import timezone

from buildblock.apps.core import constants
from buildblock.apps.management.models import Lease
from buildblock.apps.payments.constants import CURRENCY_USD
from buildblock.apps.payments.models import PaymentTransfers, RentPayment
from buildblock.apps.property.constants import PropertyCallEnum
from buildblock.apps.property.handlers.zillow import ZillowPropertyHandler
from buildblock.apps.property.models import PropertySubscriptionFilter
from buildblock.helper import db_update
from buildblock.logging import setup_logging
from buildblock.services.management import ManagementService, replace_last_date_for_month
from buildblock.services.messaging import MessagingService
from buildblock.services.stripe import StripeService
from buildblock.services.user import UserService
from buildblock.utils import sum_field

# TODO: Move this to somewhere else later
# This configures how and where to output out logs. Only need to be run once.
setup_logging()
logger = logging.getLogger(__name__)
bg_logger = logging.getLogger('background_task')
bg_logger.setLevel(logging.WARNING)

_TWELVE_HOURS_IN_SECONDS = 60 * 60 * 12
_RENT_CHARGE_WINDOW = 10        # Start creating charges, 10 days before the payment day
_GRACE_PERIOD_FOR_OVERDUE = 5   # Create overdue fees, 5 days after the payment due date
_PAYMENT_NOTIFICATION_DAYS = 3  # Payment request before the payment due date
_PAYMENT_REPORT_MONTHS = 1  # Payment request before the payment due date


def _schedule_time_set(input_datetime, new_hour: int):
    new_datetime = input_datetime.replace(second=0, microsecond=0, minute=0, hour=new_hour)
    if int(input_datetime.hour) >= new_hour:
        new_datetime = new_datetime + timedelta(days=1)
    return new_datetime


class BackgroundJobScheduler:
    @classmethod
    def schedule(cls):
        cls.stripe_transfer(repeat=Task.HOURLY)
        cls.charge_rent(repeat=Task.DAILY)
        # cls.charge_overdue(repeat=Task.DAILY)
        cls.autopay_rent(repeat=Task.DAILY)
        cls.send_messaging_requests(repeat=Task.HOURLY)
        cls.rent_payment_request(
            repeat=Task.DAILY,
            schedule=_schedule_time_set(timezone.now(), 17)  # GMT 01:00
            # TODO: User 거주 시간에 맞춰서 메일 발송
        )
        cls.rent_payment_report(
            repeat=Task.DAILY,
            schedule=_schedule_time_set(timezone.now(), 17)  # GMT 01:00
            # TODO: User 거주 시간에 맞춰서 메일 발송
        )
        cls.property_subscription(
            repeat=Task.DAILY,
            schedule=_schedule_time_set(timezone.now(), 1)  # GMT 01:00
        )

    @staticmethod
    @background(name='stripe_transfer')
    def stripe_transfer():
        pending_transfers = PaymentTransfers.objects.filter(
            account_type='stripe',
            status=constants.PENDING,
        ).order_by('created_at')

        if not pending_transfers:
            return

        source_types = pending_transfers.values_list(
            'source_type', flat=True
        ).order_by('source_type').distinct()

        for source_type in source_types:
            pending_transfers_source_type = pending_transfers.filter(source_type=source_type)
            if not pending_transfers_source_type:
                continue

            balance = StripeService.get_balance(source_type=source_type)
            if balance <= 0:
                continue

            transfer_amount = 0
            for transfer_object in pending_transfers_source_type:
                # If the transfer is about to fail due to insufficient balance, just finish early
                transfer_amount += transfer_object.amount
                if transfer_amount > balance:
                    break

                try:
                    StripeService.transfer(amount=transfer_object.amount,
                                           currency=transfer_object.currency,
                                           stripe_account=transfer_object.destination_account,
                                           source_type=transfer_object.source_type,
                                           transfer_group=transfer_object.identifier)
                except Exception as e:
                    db_update(transfer_object, dict(
                        status=constants.FAILED_OTHER_REASON
                    ))
                    logger.warning(f'Transfer to Owner ID "{transfer_object.owner.id}" failed. Details: {str(e)}')
                else:
                    db_update(transfer_object, dict(
                        status=constants.COMPLETE,
                        transfer_datetime=datetime.utcnow()
                    ))
                    logger.info(f'Completed transferring money to to Owner ID "{transfer_object.owner.id}"')

    @staticmethod
    @background(name='charge_rent')
    def charge_rent():
        # When the number of leases is small, safer to go through all.
        # Perhaps, we can later limit this to payment day += 3 days
        active_leases = Lease.objects.filter(status=constants.ACTIVE)
        for lease in active_leases:
            try:
                # Get recent payment due date for a given lease. The payment should at least be charged or already paid.
                latest_due_date = RentPayment.objects.filter(
                    tenant=lease.tenant,
                    product=lease.product,
                    payment_type=constants.RENT,
                    due_date__isnull=False
                ).latest('due_date').due_date

            except RentPayment.DoesNotExist:
                # If there is no latest rent payment, that would mean the lease is about to start, i.e., not started
                # Then just charge the first rent based on numbers of days left for the given month and continue
                latest_due_date = ManagementService.create_first_rent_payment(lease).due_date
                logger.info(
                    f'User-{lease.tenant.id}\'s first rent payment is registered : Due date - {str(latest_due_date)}')

            # replace the day as the latest due date as it might have the "day" of the lease start date
            next_due_date = replace_last_date_for_month(
                date_value=latest_due_date + relativedelta(months=1),
                replace_day=lease.payment_day
            )

            # Create rent charges that fall within our rent charging window.
            # We should only create those that are due within the next _RENT_CHARGE_WINDOW days
            cut_off_date = date.today() + relativedelta(days=_RENT_CHARGE_WINDOW)
            while (next_due_date <= cut_off_date):
                ManagementService.create_rent_payment(lease, next_due_date)
                logger.info(f'User-{lease.tenant.id}\'s new rent payment is registered : '
                            f'Due date - {str(next_due_date)}')
                next_due_date = replace_last_date_for_month(
                    date_value=next_due_date + relativedelta(months=1),
                    replace_day=lease.payment_day
                )

    @staticmethod
    @background(name='charge_overdue')
    def charge_overdue():
        overdue_start_date = date.today() - relativedelta(days=_GRACE_PERIOD_FOR_OVERDUE)
        pending_payments = RentPayment.objects.filter(
            status=constants.PENDING,
            due_date__isnull=False,
        )
        overdue_fees = pending_payments.filter(
            payment_type__in=[constants.RENT],
            due_date__lt=overdue_start_date,
        )
        pending_overdue_payments = pending_payments.filter(
            payment_type=constants.OVERDUE,
        ).order_by('due_date')
        for fee in overdue_fees:
            lastest_overdue_payment_by_fee = pending_overdue_payments.filter(
                linked_payment=fee
            ).last()
            request_due_date = lastest_overdue_payment_by_fee.due_date \
                if lastest_overdue_payment_by_fee else fee.due_date
            while (request_due_date < overdue_start_date):
                # TODO: Asset팀과 논의 후 overdue payment 설정 작업 예정
                request_due_date = request_due_date + relativedelta(months=1)
                payment = ManagementService.create_overdue_payment(
                    payment=fee,
                    due_date=request_due_date,
                )
                logger.info(f'The overdue fee request has been submitted: payment_id={payment.id}')

    @staticmethod
    @background(name='autopay_rent')
    def autopay_rent():
        # TODO: We might have to initiate this one day earlier to get this actually paid on the payment day
        today = date.today()
        auto_paid_leases = Lease.objects.filter(
            status=constants.ACTIVE,
            payment_day=today.day,
            is_auto_paid=True,
        )
        for lease in auto_paid_leases:
            unpaid_rents = RentPayment.objects.filter(
                tenant=lease.tenant,
                product=lease.product,
                payment_type=constants.RENT,
                status=constants.PENDING,
                due_date__lte=today,
            )
            try:
                payment = StripeService.create_charge_by_bank_account(
                    user_model=lease.tenant,
                    product_id=lease.product.id,
                    amount=sum_field(unpaid_rents, 'amount'),
                    currency=CURRENCY_USD,
                    bank_id=lease.tenant.profile_tenant.auto_payment_account_id,
                )
            except Exception as e:
                # No special exception handling here. Just fail open as this is an async background job
                # We should not mark these as "FAILED" as the user should at least be capable of paying
                # this manually.
                # TODO: come up with a better recovery/logging process
                logger.error(f'Auto payment failed: {str(e)} user_id={lease.tenant.id} product_id={lease.product.id}')
            else:
                payment_identifier = payment.transfer_group.split(':')[-1]
                data_dict = dict(
                    status=constants.IN_PROGRESS,
                    payment_method=constants.ACH_DEBIT,
                    payment_made_datetime=datetime.utcnow(),
                    identifier=payment_identifier,
                )
                db_update(unpaid_rents, data_dict)
                logger.info(f'The ACH auto-payment request has been submitted: payment_id={payment.id}')

    @staticmethod
    @background(name='rent_payment_request')
    def rent_payment_request():
        # Payment Request Email.
        # Send notification mail on the due date and a specific number of days before the due date.
        today = date.today()
        due_date_for_notification = today + relativedelta(days=_PAYMENT_NOTIFICATION_DAYS)
        unpaid_payments = ManagementService.get_payments_by_filters(statuses=[constants.PENDING])
        tenant_id_lists = unpaid_payments.filter(
            Q(due_date=today) | Q(due_date=due_date_for_notification)
        ).values_list('tenant', flat=True).order_by('tenant').distinct()
        for tenant_id in tenant_id_lists:
            try:
                payment_list = unpaid_payments.filter(tenant__id=tenant_id).order_by('due_date')
                MessagingService.schedule_payment_request_email(
                    payment_list=payment_list,
                    tenant=payment_list.first().tenant,
                )
            except Exception as e:
                logger.error(f'Payment Request Failed: {str(e)} user_id={tenant_id}')
                continue

    @staticmethod
    @background(name='rent_payment_report')
    def rent_payment_report():
        # Payment Reporting Email for Agency.
        today = date.today()
        start_date_for_report = today - relativedelta(months=_PAYMENT_REPORT_MONTHS)
        agencies = UserService.get_groups_by_category(constants.AGENCY)
        for agency in agencies:
            payment_data_for_report = []
            for product in agency.products.all():
                payments = product.rent_payments_product.order_by('tenant')
                paid_payments = payments.filter(
                    status__in=[constants.COMPLETE, constants.IN_PROGRESS],
                    due_date__gte=start_date_for_report,
                )
                unpaid_payments = payments.filter(
                    status=constants.PENDING
                )
                if paid_payments or unpaid_payments:
                    payment_data_for_report.append({
                        'product': product,
                        'paid_payments': paid_payments,
                        'unpaid_payments': unpaid_payments,
                    })
            if not payment_data_for_report:
                continue
            try:
                MessagingService.schedule_payment_report_email(
                    payment_data=payment_data_for_report,
                    agency=agency,
                )
            except Exception as e:
                logger.error(f'Payment Request Failed: {str(e)}')

    @staticmethod
    @background(name='send_messaging_requests')
    def send_messaging_requests():
        messaging_requests = MessagingService.get_messaging_request_standby_list()
        for messaging in messaging_requests:
            try:
                if MessagingService.send_message(
                    title=messaging.title,
                    content=messaging.content,
                    receiver_emails=messaging.receivers,
                    sender_email=messaging.sender,
                ):
                    messaging.sent_at = timezone.now()
                    db_update(messaging)
            except Exception as e:
                logger.error(f'Sending Messaging Request Failed: {str(e)} id={messaging.id}')
                continue

    @staticmethod
    @background(name='property_subscription')
    def property_subscription():
        filter_list = PropertySubscriptionFilter.objects.filter(
            status=constants.ACTIVE,
        )
        for single_filter in filter_list:
            if not single_filter.messaging_template:
                logger.error(f"The messaging template for the property email subscription does not exist. \
                               - Filter: {str(single_filter.id)} {single_filter.title}")
                continue
            try:
                handler = ZillowPropertyHandler(
                    type=PropertyCallEnum.PROPERTY_SALE_LIST,
                    data=dict(single_filter.filter)
                )
                property_list = handler.run()['properties']
            except Exception as e:
                logger.error(f'Property list generation failed: {str(e)} filter_id={single_filter.id}')
            else:
                property_list_for_email = []
                last_sent = None
                for property in property_list:
                    list_date = property.list_date.astimezone(pytz.utc)
                    if not single_filter.last_sent or list_date > single_filter.last_sent:
                        property_detail = ZillowPropertyHandler(
                            type=PropertyCallEnum.PROPERTY_DETAIL,
                            data=dict(property_id=property.id)
                        ).run()['property']
                        property_list_for_email.append(property_detail)
                        if not last_sent or list_date > last_sent:
                            last_sent = list_date
                if property_list_for_email:
                    MessagingService.send_property_list_email(property_list_for_email, single_filter)
                    logger.info(f'{len(property_list_for_email)} properties data has been sent: {single_filter.title}')
                if last_sent:
                    single_filter.last_sent = last_sent
                    db_update(single_filter)
