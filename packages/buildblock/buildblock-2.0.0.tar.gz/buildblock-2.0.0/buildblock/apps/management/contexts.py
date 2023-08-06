from buildblock.apps.core.constants import (
    ACH_DEBIT,
    ACTIVE,
    COMPLETE,
    CREDIT_CARD,
    CREDIT_CARD_CHARGE_RATE,
    IN_PROGRESS,
    PENDING,
    RENT,
    TENANT_ROLE
)
from buildblock.apps.payments.models import RentPayment
from buildblock.apps.product.models import Product as ProductDataModel
from buildblock.models.management import Lease, Owner
from buildblock.models.payments import ActualPaymentAmount, Payments
from buildblock.models.product import Amenities, Product, ProductImage
from buildblock.services.stripe import StripeService
from buildblock.utils import calculate_payment_fee, safe_money_read_from_db, sum_field


class ManagementContext:
    def _make_lease_context(self, lease):
        return Lease(
            id=lease.id,
            full_address=lease.product.full_address,
            room_num=lease.room_num,
            status=lease.status,
            owner_name=lease.owner.name,
            tenant_name=lease.tenant.name,
            start_date=lease.start_date,
            end_date=lease.end_date,
            rent=safe_money_read_from_db(lease.rent),
            deposit=safe_money_read_from_db(lease.deposit),
            payment_day=lease.payment_day,
            tenant_phone_number=lease.tenant.phone_number,
            tenant_email=lease.tenant.email,
            tenant_credit_score=lease.tenant.credit_score,
            num_paid_rents=lease.num_paid_rents,
            created_at=lease.created_at.date(),
            is_auto_paid=lease.is_auto_paid,
        )

    def _make_all_leases_context(self, product):
        _status_list = [ACTIVE, PENDING, COMPLETE]
        leases = sorted(
            product.lease_product.all(),
            key=lambda x: _status_list.index(x.status)
        )
        return [
            self._make_lease_context(lease)
            for lease in leases
        ]

    def _make_product_context(self, product: ProductDataModel):
        product_images = [
            ProductImage(
                title=product.full_address,
                original_image_url=product.main_image.url,
                thumbnail_image_url=product.main_thumbnail_image_url,
            )
        ] + [
            ProductImage(
                title=product_image.title,
                original_image_url=product_image.image.url,
                thumbnail_image_url=product_image.thumbnail_image_url,
            )
            for product_image in product.images.all()
        ]
        product_context = Product(
            id=product.id,
            code=product.code,
            description=product.description,
            full_address=product.full_address,
            main_image_url=product.main_image.url,
            plan_image_url=product.plan_image.url if product.plan_image else None,
            max_num_people=product.num_people,
            num_people_under_lease=product.active_leases.count(),
            rent_under_lease=safe_money_read_from_db(sum_field(product.active_leases, 'rent')),
            deposit_under_lease=safe_money_read_from_db(sum_field(product.active_leases, 'deposit')),
            status=product.status,
            added_at=product.created_at.date(),
            num_bedroom=product.num_bedroom,
            num_bathroom=product.num_bathroom,
            num_parking=product.num_parking,
            map_url=product.map_url,
            property_type=product.get_property_type_display(),
            sqft=product.sqft,
            lot_sqft=product.lot_sqft,
            washer_dryer=product.washer_dryer,
            allowed_pets=product.allowed_pets,
            built_year=product.built_year,
            amenities=Amenities(
                heater=product.amenities.get("heater"),
                cooling=product.amenities.get("cooling"),
            ),
            product_images=product_images,
            owners=product.owner.all(),
            agency=product.agency
        )

        return product_context

    def _make_payments_context(self, product):
        # prevent misuse by guarding
        if self.active_role != TENANT_ROLE:
            return None
        rent_payments = RentPayment.objects.filter(
            tenant=self.request.user,
            product=product,
        )
        unpaid_amount = sum_field(rent_payments.filter(status=PENDING), 'amount')
        payment_in_progress_amount = sum_field(rent_payments.filter(status=IN_PROGRESS), 'amount')
        card_fee = calculate_payment_fee(CREDIT_CARD, unpaid_amount)
        card_payment = ActualPaymentAmount(
            amount=safe_money_read_from_db(unpaid_amount + card_fee),
            fee=safe_money_read_from_db(card_fee),
            fee_rate=CREDIT_CARD_CHARGE_RATE,
        )
        ach_debit_fee = calculate_payment_fee(ACH_DEBIT, unpaid_amount)
        ach_debit_fee_rate = round((ach_debit_fee / unpaid_amount), 2) if unpaid_amount > 0 else 0
        ach_debit_payment = ActualPaymentAmount(
            amount=safe_money_read_from_db(unpaid_amount + ach_debit_fee),
            fee=safe_money_read_from_db(ach_debit_fee),
            fee_rate=ach_debit_fee_rate,
        )
        return Payments(
            unpaid_amount=safe_money_read_from_db(unpaid_amount),
            payment_in_progress_amount=safe_money_read_from_db(payment_in_progress_amount),
            card_payment=card_payment,
            ach_debit_payment=ach_debit_payment,
            rent_count=rent_payments.filter(status=COMPLETE, payment_type=RENT).count()
        )

    def _make_owner_context(self, owner):
        products = owner.owned_products.all() & self.products \
            if self.products else owner.owned_products.all()
        products = [
            self._make_product_context(product)
            for product in products
        ]
        profile = owner.profile_owner
        stripe_account_id = profile.stripe_account if profile else None
        total_balance_amount = 0
        available_balance_amount = 0
        if stripe_account_id:
            # Balance
            stripe_balance = StripeService.get_account_balance(
                stripe_account=stripe_account_id
            )
            for key, value in stripe_balance.items():
                stripe_balance[key] = safe_money_read_from_db(value)
            total_balance_amount = stripe_balance.get('total_balance_amount', 0)
            available_balance_amount = stripe_balance.get('available_balance_amount', 0)
        return Owner(
            id=owner.id,
            name=owner.name,
            email=owner.email,
            phone_number=owner.phone_number,
            nationality=owner.nationality,
            full_address=profile.full_address,
            products=products,
            stripe_account=stripe_account_id,
            total_balance_amount=total_balance_amount,
            available_balance_amount=available_balance_amount
        )

    def _make_all_owners_context(self, owners):
        return [
            self._make_owner_context(owner)
            for owner in owners
        ]
