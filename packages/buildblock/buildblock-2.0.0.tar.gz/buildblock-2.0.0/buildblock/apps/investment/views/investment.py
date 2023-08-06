'''
투자 리스트와 투자 상세 페이지 등 투자 정보 View
- Model "Investment" 기준으로 서비스 제공
'''

from buildblock.apps.core.views import DetailView, ListView
from buildblock.apps.investment.models import Investment, InvestmentContract
from buildblock.apps.investment.views.base import InvestmentServiceMixin
from buildblock.apps.management.contexts import ManagementContext
from buildblock.apps.product.models import Product


class InvestmentBaseView(InvestmentServiceMixin, ManagementContext):
    model = Investment
    page_title = "Investment"
    context_object_name = "investment"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)


class InvestmentListView(InvestmentBaseView, ListView):
    page_title = "Investment List"
    context_object_name = "investments"


class InvestmentDetailView(InvestmentBaseView, DetailView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        investment = self.object
        products = Product.objects.filter(
            investment_product=investment.investment_product
        )
        context['products'] = [
            self._make_product_context(product)
            for product in products
        ]
        documents = InvestmentContract.objects.filter(
            investment=investment
        )
        context['documents'] = [
            self._make_investment_contract_context(document)
            for document in documents
        ]
        return context
