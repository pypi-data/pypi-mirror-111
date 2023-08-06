import logging
from calendar import monthrange

from dateutil.relativedelta import relativedelta
from django.forms import ValidationError

from buildblock.apps.core.constants import DEPOSIT, LIVE_LEASE_STATUS, OVERDUE, PENDING, RENT
from buildblock.apps.management.models import Lease, Maintenance
from buildblock.apps.payments.models import RentPayment
from buildblock.apps.users.models import User
from buildblock.errors import InvalidParameterError
from buildblock.mixins import Loggable

logger = logging.getLogger(__name__)

_OVERDUE_FEE_RATE = 0.05


def replace_last_date_for_month(date_value, replace_day):
    # If replace_day is out of range for month, it is set as the last day.
    try:
        return date_value.replace(day=replace_day)
    except ValueError:
        return date_value.replace(day=monthrange(date_value.year, date_value.month)[1])


def _calculate_prorated_rent(lease):
    lease_start_date = lease.start_date
    payment_date_of_this_month = replace_last_date_for_month(lease_start_date, lease.payment_day)
    if lease_start_date.day < lease.payment_day:
        payment_date_of_prev_month = replace_last_date_for_month(
            lease_start_date - relativedelta(months=1), lease.payment_day)
        days_in_month = (payment_date_of_this_month - payment_date_of_prev_month).days
        days_left_in_month = (payment_date_of_this_month - lease_start_date).days
    else:
        payment_date_of_next_month = replace_last_date_for_month(
            lease_start_date + relativedelta(months=1), lease.payment_day)
        days_in_month = (payment_date_of_next_month - payment_date_of_this_month).days
        days_left_in_month = (payment_date_of_next_month - lease_start_date).days
    return int(lease.rent * days_left_in_month / days_in_month)


class ManagementService(Loggable):
    """Service that interacts with the databases in the Management service"""

    @classmethod
    def create_lease(cls, *, room_num, owner, tenant, product, start_date, end_date, rent, deposit):
        if start_date <= end_date:
            cls.logger.error(f'Used arguments for creating a lease: {locals()}')
            raise InvalidParameterError

        Lease.objects.create(
            room_num=room_num,
            owner=owner,
            tenant=tenant,
            product=product,
            status=PENDING,
            start_date=start_date,
            end_date=end_date,
            rent=rent,
            deposit=deposit,
        )

    @classmethod
    def create_payment(cls, tenant, product, amount, payment_type, due_date, linked_payment=None):
        return RentPayment.objects.create(
            tenant=tenant,
            product=product,
            amount=amount,
            status=PENDING,
            payment_type=payment_type,
            due_date=due_date,
            linked_payment=linked_payment,
        )

    @classmethod
    def create_deposit_payment(cls, lease):
        return cls.create_payment(
            tenant=lease.tenant,
            product=lease.product,
            amount=lease.deposit,
            payment_type=DEPOSIT,
            due_date=lease.start_date,
        )

    @classmethod
    def create_rent_payment(cls, lease, due_date):
        return cls.create_payment(
            tenant=lease.tenant,
            product=lease.product,
            amount=lease.rent,
            payment_type=RENT,
            due_date=due_date,
        )

    @classmethod
    def create_first_rent_payment(cls, lease):
        return cls.create_payment(
            tenant=lease.tenant,
            product=lease.product,
            amount=_calculate_prorated_rent(lease),
            payment_type=RENT,
            due_date=lease.start_date,
        )

    @classmethod
    def create_overdue_payment(cls, payment, due_date):
        overdue_fee_amount = payment.amount * _OVERDUE_FEE_RATE
        return cls.create_payment(
            tenant=payment.tenant,
            product=payment.product,
            amount=overdue_fee_amount,
            payment_type=OVERDUE,
            due_date=due_date,
            linked_payment=payment,
            linked_reason=OVERDUE,
        )

    @classmethod
    def get_lease_by_id(cls, id):
        return Lease.objects.get(id=id)

    @classmethod
    def get_leases_by_filters(cls, products=[], statuses=[]):
        query = {}
        if products:
            query['product__in'] = products
        if statuses:
            query['status__in'] = statuses
        if query:
            return Lease.objects.filter(**query)
        return []

    @classmethod
    def get_live_leases_by_products(cls, products):
        return cls.get_leases_by_filters(
            products=products,
            statuses=LIVE_LEASE_STATUS,
        )

    @classmethod
    def get_duplication_live_leases(cls, lease):
        return Lease.objects.filter(
            product=lease.product,
            tenant=lease.tenant,
            status__in=LIVE_LEASE_STATUS,
        ).exclude(id=lease.id)

    @classmethod
    def duplication_live_lease_validation(cls, lease):
        # Duplicate Live Lease Validation
        live_leases = cls.get_duplication_live_leases(lease)
        if lease.status in LIVE_LEASE_STATUS and live_leases:
            raise ValidationError(
                "There is a duplicate lease. Please modify the existing lease.")

    @classmethod
    def get_maintenances_by_filters(cls, tenants=[], products=[]):
        query = {}
        if tenants:
            query['tenant__in'] = tenants
        if products:
            query['product__in'] = products
        if query:
            return Maintenance.objects.filter(**query)
        return []

    @classmethod
    def get_tenants_by_products(cls, products):
        return User.objects.filter(
            lease_tenant__product__in=products
        )

    @classmethod
    def get_live_tenants_by_products(cls, products):
        return cls.get_tenants_by_products(products).filter(
            lease_tenant__status__in=LIVE_LEASE_STATUS
        )

    @classmethod
    def get_payments_by_filters(cls, tenants=[], products=[], statuses=[]):
        query = {}
        if tenants:
            query['tenant__in'] = tenants
        if products:
            query['product__in'] = products
        if statuses:
            query['status__in'] = statuses
        if query:
            return RentPayment.objects.filter(**query)
        return []
