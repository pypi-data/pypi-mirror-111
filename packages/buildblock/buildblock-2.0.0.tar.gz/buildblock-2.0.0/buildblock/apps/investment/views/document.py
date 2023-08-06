'''
투자 계약서와 첨부 문서 등 투자 정보를 제공하는
- Model "investment.models > InvestmentContract" 기준으로 서비스 제공
'''
from private_storage.views import PrivateStorageDetailView

from buildblock.apps.core.constants import SIG_NOT_REQUIRED_COMPLETE, SIG_NOT_REQUIRED_PENDING
from buildblock.apps.core.models import add_read_data_at_record
from buildblock.apps.core.views import ListView
from buildblock.apps.investment.models import InvestmentContract, InvestmentProduct
from buildblock.apps.investment.views.base import InvestmentServiceMixin
from buildblock.helper import db_update


class DocumentView(InvestmentServiceMixin):
    model = InvestmentContract


class DocumentListView(DocumentView, ListView):
    template_name = "investment/document_list.html"
    context_object_name = "documents"

    def with_investment_product_id_filter(self, queryset):
        id = self.request.GET.get('investment_product')
        return queryset.filter(investment__investment_product__id=id) if id else queryset

    def get_queryset(self):
        queryset = super().get_queryset().filter(investment__user=self.request.user)
        queryset = self.with_investment_product_id_filter(queryset)
        return queryset.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        documents = context[self.context_object_name]
        context[self.context_object_name] = [
            self._make_investment_contract_context(document)
            for document in documents
        ]
        context['investment_products'] = InvestmentProduct.objects.filter(
            investments__user=self.request.user
        )

        return context


class DocumentDownloadView(DocumentView, PrivateStorageDetailView):
    model_file_field = 'document_file'

    def get(self, request, *args, **kwargs):
        self.object = contract = self.get_object()
        # Status Change: Unread > Read
        if not (contract.status == SIG_NOT_REQUIRED_PENDING and contract.investment.user == self.request.user):
            contract.status = SIG_NOT_REQUIRED_COMPLETE
        # Append Read Data in Record
        contract.records = add_read_data_at_record(contract.records, self.request.user)
        db_update(contract)
        return super().get(request, *args, **kwargs)
