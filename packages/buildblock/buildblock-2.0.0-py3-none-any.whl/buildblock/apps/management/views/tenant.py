
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse

from buildblock.apps.core.constants import AGENT_ROLE, COMPLETE, OWNER_ROLE, RENT
from buildblock.apps.management.forms import LeaseCreateForm, LeaseUpdateForm
from buildblock.apps.management.models import Lease
from buildblock.apps.management.views.base import (
    ManagementCreateView,
    ManagementDetailView,
    ManagementTemplateView,
    ManagementUpdateView
)
from buildblock.apps.product.models import Product
from buildblock.apps.users.mixin import ViewPermissionCheckMixin
from buildblock.models.product import Product as ProductContext
from buildblock.services.management import ManagementService
from buildblock.utils import safe_money_read_from_db, safe_money_save_from_dollar

_MAX_MAINTENANCE_LIST_SIZE = 10
_MAX_TRANSACTION_LIST_SIZE = 10


'''
Owner 유저가 보유한 집의 Tenant 전체리스트

개발담당: -

이용자: Owner

페이지 목적: Owner가 Tenant의 현재 상황을 한번에 확인하는 곳으로
            현재 보유한 집(Product)을 기준으로 Tenant의 기본 정보와
            계약 및 월세 현황(완료, n개월 연체, 보증금, 계약 날짜)을
            확인 할 수 있는 곳
주의점:
    1. Tenant 유저가 가입을 하지 않는 경우에 대한 대비
        - 주인이 기록용 으로 서비스를 사용을 할 수 있도록
           Tenant 유저 가입전에 임의로 Tenant 정보를 입력하고
           사용 가능하게 서비스 개발을 해야함
           (추후에 회의)
'''


class ManagementTenantMixin(ViewPermissionCheckMixin):
    permitted_role_list = [OWNER_ROLE, AGENT_ROLE]


class ManagementTenantListView(ManagementTenantMixin, ManagementTemplateView):
    template_name = "management/tenant-list.html"
    page_title = "Tenants"

    def _get_mapped_leases(self, product_context: ProductContext):
        product = Product.objects.get(id=product_context.id)
        leases = self._make_all_leases_context(product)
        return leases

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = context.get('products')
        if products:
            context['leases'] = list(map(self._get_mapped_leases, products))
        return context


class ManagementTenantDetailView(ManagementTenantMixin, ManagementDetailView):
    template_name = "management/tenant-detail.html"
    model = Lease
    context_object_name = "lease"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.product not in self.products:
            raise Http404
        return obj

    def get_context_data(self, **kwargs):
        self.object = lease = self.get_object()
        context = super().get_context_data(**kwargs)
        # Transactions
        all_transactions = ManagementService.get_payments_by_filters(
            tenants=[lease.tenant],
            products=[lease.product],
        ).order_by('-id')
        transactions = all_transactions[:_MAX_TRANSACTION_LIST_SIZE]
        more_transactions = True if all_transactions.count() > 10 else False
        # Rent Payment
        rent_count = all_transactions.filter(
            status=COMPLETE,
            payment_type=RENT
        ).count()
        # Maintenaces
        maintenances = ManagementService.get_maintenances_by_filters(
            tenants=[lease.tenant],
            products=[lease.product]
        ).order_by('-id')[:_MAX_MAINTENANCE_LIST_SIZE]

        context.update(
            tenant=lease.tenant,
            lease=self._make_lease_context(lease),
            product=self._make_product_context(lease.product),
            transactions=transactions,
            maintenances=maintenances,
            rent_count=rent_count,
            more_transactions=more_transactions
        )

        return context


class ManagementLeaseFormView(ManagementTenantMixin):
    model = Lease

    def form_valid(self, form):
        lease = form.save(commit=False)
        lease.rent = safe_money_save_from_dollar(lease.rent)
        lease.deposit = safe_money_save_from_dollar(lease.deposit)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('management:tenant-detail', kwargs={'pk': self.object.id})


class ManagementLeaseCreateView(ManagementLeaseFormView, ManagementCreateView):
    form_class = LeaseCreateForm
    template_name = "management/lease-create.html"
    page_title = "Create Lease"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['product_list'] = self.products.filter(code=self.kwargs.get('product_code'))
        return kwargs

    def form_valid(self, form):
        # Create Lease
        lease = form.save(commit=False)
        try:
            ManagementService.duplication_live_lease_validation(lease)
        except ValidationError as e:
            messages.error(self.request, e.message)
            return self.form_invalid(form)
        super().form_valid(form)
        # Create Payment
        # super().form_valid(form)를 통해 self.object에 DB에 저장 된 lease가 할당
        lease = self.object
        if form.cleaned_data.get('payment_deposit'):
            ManagementService.create_deposit_payment(lease)
        if form.cleaned_data.get('payment_rent'):
            ManagementService.create_first_rent_payment(lease)
        return HttpResponseRedirect(self.get_success_url())


class ManagementLeaseUpdateView(ManagementLeaseFormView, ManagementUpdateView):
    form_class = LeaseUpdateForm
    template_name = "management/lease-update.html"
    page_title = "Edit Lease"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.rent = safe_money_read_from_db(obj.rent)
        obj.deposit = safe_money_read_from_db(obj.deposit)
        return obj
