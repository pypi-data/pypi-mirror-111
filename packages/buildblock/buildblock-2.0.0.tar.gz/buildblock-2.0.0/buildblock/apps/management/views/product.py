from datetime import date

from dateutil.relativedelta import relativedelta
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from buildblock.apps.core.constants import (
    AGENCY,
    AGENT_ROLE,
    COMPLETE,
    OWNER_ROLE,
    RENT,
    SIG_NOT_REQUIRED_PENDING,
    SIG_REQUIRED_PENDING
)
from buildblock.apps.management.forms import ProductForm
from buildblock.apps.management.models import Maintenance
from buildblock.apps.management.views.base import (
    ManagementCreateView,
    ManagementDetailView,
    ManagementTemplateView,
    ManagementUpdateView
)
from buildblock.apps.payments.models import RentPayment
from buildblock.apps.product.models import Product
from buildblock.apps.users.mixin import ViewPermissionCheckMixin
from buildblock.utils import safe_money_read_from_db

_MAX_MAINTENANCE_LIST_SIZE = 5
_MIN_PRODUCT_PAGE_CONTRACT_LIST_SIZE = 5
_PRODUCT_PAGE_CONTRACT_STATUS_LIST = [SIG_REQUIRED_PENDING, SIG_NOT_REQUIRED_PENDING]


def generate_product_code(product):
    '''{state code}{zip code}-{number>=1}'''
    if product.code:
        return product.code
    base_code_format = f'{product.state}{product.zip_code}-'
    product_list = Product.objects.filter(code__contains=base_code_format).order_by('-id')
    product_code_list = product_list.values_list('code', flat=True)
    if not product_code_list:
        return f'{base_code_format}1'
    number = int(product_code_list[0].split('-')[-1]) + 1
    return f'{base_code_format}{str(number)}'


class ManagementProductMixin(ViewPermissionCheckMixin):
    permitted_role_list = [AGENT_ROLE, OWNER_ROLE]


class ManagementProductListView(ManagementProductMixin, ManagementTemplateView):
    page_title = "Product List"
    template_name = "management/product-list.html"


class ManagementProductDetailView(ManagementProductMixin, ManagementDetailView):

    def get_object(self):
        return get_object_or_404(Product, code=self.kwargs.get('product_code'))

    def get_context_data(self, **kwargs):
        self.object = product = self.get_object()
        context = super().get_context_data(**kwargs)
        context['product'] = self._make_product_context(product)

        # There is no product associated with 'product_code'.
        if not product:
            return self._error_message_and_redirect(
                context=context,
                error_message=_('Something went wrong. Please try again.'),
                redirect_url=reverse('management:product-list'),
            )

        return context


class ManagementProductInfoView(ManagementProductDetailView):
    template_name = "management/product-info.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object

        context['leases'] = self._make_all_leases_context(product)
        context['maintenances'] = Maintenance.objects.filter(
            product=product
        ).all().order_by('-created_at')[:_MAX_MAINTENANCE_LIST_SIZE]

        # Income Chart Data
        payments = RentPayment.objects \
            .filter(
                product=product,
                payment_type=RENT,
                status=COMPLETE,
                payment_made_datetime__isnull=False
            ) \
            .annotate(month=TruncMonth('payment_made_datetime')).values('month') \
            .annotate(sum=Sum('amount')).values('month', 'sum') \
            .order_by('month')

        income_data = {}
        for i in range(12):
            i_date = date.today() - relativedelta(months=11-i)
            income_data[i_date.strftime('%b.%y')] = 0

        for payment in payments:
            payment_month = payment['month'].strftime('%b.%y')
            if payment_month in income_data:
                income_data[payment_month] = safe_money_read_from_db(payment['sum'])

        context['income_chart_label'] = str(list(income_data.keys()))
        context['income_chart_data'] = str(list(income_data.values()))

        income_chart_step = int(round(max(list(income_data.values())) / 10, -2))
        context['income_chart_step'] = income_chart_step if income_chart_step > 10 else 10

        return context


class ManagementProductFormView(ManagementProductMixin):
    model = Product
    form_class = ProductForm
    template_name = "management/product-form.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['agency_groups'] = self.request.user.groups.filter(detail__category=AGENCY)
        return kwargs

    def get_success_url(self):
        return reverse(
            'management:product-info',
            kwargs={'product_code': self.object.code}
        )


class ManagementProductCreateView(ManagementProductFormView, ManagementCreateView):
    page_title = "Create Product"

    def form_valid(self, form):
        self.object = product = form.save(commit=False)
        product.code = generate_product_code(product)
        return super().form_valid(form)


class ManagementProductUpdateView(ManagementProductFormView, ManagementUpdateView):
    page_title = "Edit Product"
