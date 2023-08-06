import json
import logging

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from docusign_esign.client.api_exception import ApiException

from buildblock.apps.administrator.views.base import AdministratorServiceMixin
from buildblock.apps.core.constants import (
    BUILDBLOCK_EMAIL,
    BUILDBLOCK_ID,
    BUILDBLOCK_NAME,
    BUILDBLOCK_ROLE,
    COMPLETE,
    IN_PROGRESS,
    INVESTMENT,
    PENDING,
    SIGNATURE
)
from buildblock.apps.core.views import CreateView, DeleteView, DetailView, ListView, UpdateView
from buildblock.apps.investment.contexts import InvestmentContext
from buildblock.apps.investment.forms import (
    ContractTemplateForm,
    InvestmentContractForm,
    InvestmentForm,
    InvestmentProductForm,
    InvestmentStepForm
)
from buildblock.apps.investment.models import (
    ContractTemplate,
    Investment,
    InvestmentContract,
    InvestmentProduct,
    InvestmentStep
)
from buildblock.apps.management.contexts import ManagementContext
from buildblock.apps.product.models import Product
from buildblock.apps.users.models import User
from buildblock.helper import db_update
from buildblock.models.investment import InvestmentModel, InvestmentStageModel
from buildblock.services.docusign import DocusignService
from buildblock.services.email import EmailService
from buildblock.utils import get_investment_progress_percentage, safe_money_read_from_db, set_initial_value_field

logger = logging.getLogger(__name__)


def _create_template_role_element(email, name, role_name, user_id, routing_order):
    return {
        "email": email,
        "name": name,
        "roleName": role_name,
        "clientUserId": user_id,
        "routingOrder": routing_order
    }


def add_product_to_investment_product(request, investment_product_id, product_id):
    product = Product.objects.filter(id=product_id)
    data_dict = dict(
        investment_product=investment_product_id,
        status=INVESTMENT
    )
    db_update(product, data_dict)
    return redirect('administrator:investment-product-detail', pk=investment_product_id)


def delete_product_to_investment_product(request, investment_product_id, product_id):
    product = Product.objects.filter(id=product_id)
    db_update(product, dict(investment_product=None))
    # TODO: 건물이 투자상품에 연동이 되었다고 취소가 되면 어떤 상태로 두어야 하는지
    return redirect('administrator:investment-product-detail', pk=investment_product_id)


def create_envelope_recipient_view(request, envelope_id):
    try:
        # TODO: return_url을 통한 상태 변화 처리 업데이트
        redirect(
            DocusignService.create_recipient_view(
                envelope_id=envelope_id,
                user_name=request.user.name,
                user_email=request.user.email,
                user_id=request.user.id,
                return_url=reverse_lazy('management:product-list'),
            )
        )
    except ApiException as e:
        err = json.loads(e.body)
        logger.error(f'Error has occurred while loading envelope "{envelope_id}": {str(err)}')
        messages.warning(request, err.get('message'))
    except Exception as e:
        logger.error(f'Error has occurred while loading envelope "{envelope_id}": {str(e)}')
        messages.warning(request, f'Loading E-signature page failed. Please contact us.')

    return redirect(reverse_lazy('management:product-list'))


def envelope_document_download(request, envelope_id):
    try:
        file = DocusignService.get_document(envelope_id)
        with open(file, 'rb') as f:
            pdf_contents = f.read()
            f.close()
    except ApiException as e:
        err = json.loads(e.body)
        logger.error(f'Error has occurred while downloding esignature document: {str(err)}')
        messages.warning(request, err.get('message'))
    except Exception as e:
        logger.error(f'Error has occurred while downloding esignature document: {str(e)}')
        messages.warning(request, "Download failed. Please try again.")
    else:
        return HttpResponse(pdf_contents, content_type='application/pdf')

    return redirect('administrator:investment-product-list')


def envelope_create(investment, template):
    manager = investment.investment_product.manager
    customer = investment.user
    # Create template role elements
    manager_role = _create_template_role_element(manager.email, manager.name, "Manager", manager.id, 1)
    company_role = _create_template_role_element(BUILDBLOCK_EMAIL, BUILDBLOCK_NAME, BUILDBLOCK_ROLE, BUILDBLOCK_ID, 2)
    customer_role = _create_template_role_element(customer.email, customer.name, "Customer", customer.id, 3)

    envelope_definition = {
        "status": "sent",
        "templateId": template.identifier,
        "templateRoles": [manager_role, company_role, customer_role]
    }

    return DocusignService.create_envelope(envelope_definition)


def get_investment_step_email_data(request, step, comment=''):
    stage_list = sorted(step.investment.workflow_template.stage_list, key=lambda i: i['id'])
    stage_data = next(iter([x for x in stage_list if x['id'] == step.stage_id]), None)

    # Investment Progress
    all_steps = step.investment.investment_steps
    progress_percentage_sum = 0
    for stage in stage_list:
        stage['progress_percentage'] = get_investment_progress_percentage(
            steps=all_steps.filter(stage_id=stage.get('id')).order_by('pk')
        )
        progress_percentage_sum += stage['progress_percentage']
    total_progress_percentage = int(progress_percentage_sum / len(stage_list))

    # Site Link
    # TODO: Signed Url 교체 예정
    product_code = step.investment.investment_product.product_set.first().code
    site_link = request.build_absolute_uri(
        reverse('management:product-info', kwargs={'product_code': product_code})
    )

    return {
        'user_name': step.investment.user.name,
        'user_email': step.investment.user.email,
        'investment_title': step.investment.investment_product.title,
        'stage_title': stage_data.get('title'),
        'stage_id': stage_data.get('id'),
        'step_title': step.title,
        'status': step.get_status_display(),
        'description': step.description,
        'stage_list': stage_list,
        'total_progress_percentage': total_progress_percentage,
        'site_link': site_link,
        'comment': comment
    }


def get_investment_stage_list(investment):
    investment_stages = sorted(investment.workflow_template.stage_list, key=lambda i: i['id'])
    investment_steps = investment.investment_steps
    stage_list = []
    for stage in investment_stages:
        stage_id = stage.get('id')
        steps = investment_steps.filter(stage_id=stage_id).order_by('pk')
        if steps.count() == 0:
            continue
        progress_percentage = get_investment_progress_percentage(steps)

        if progress_percentage == 100:
            stage_status = COMPLETE
        elif progress_percentage == 0:
            stage_status = PENDING
        else:
            stage_status = IN_PROGRESS

        stage_list.append(InvestmentStageModel(
            id=stage_id,
            status=stage_status,
            title=stage.get('title'),
            description=stage.get('description'),
            progress_percentage=progress_percentage,
            steps=steps
        ))
    return stage_list


def send_investment_step_email(request):
    step_id = request.POST.get('step_id')
    comment = request.POST.get('comment')
    step = InvestmentStep.objects.get(id=step_id)
    email_data = get_investment_step_email_data(request, step, comment)
    result = EmailService.send_investment_step_email(email_data)
    if result:
        messages.success(request, "Email delivery success.")
    else:
        messages.warning(request, "Email delivery failure.")
    return redirect(reverse_lazy(
        'administrator:investment-detail',
        kwargs={'pk': step.investment.id}
    ))


# INVESTMENT
class InvestmentMixin(InvestmentContext, AdministratorServiceMixin):
    model = Investment
    page_title = "Investment"
    context_object_name = "investment"
    form_class = InvestmentForm
    template_name = "administrator/base_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            page_title=self.page_title,
        )
        return context

    def get_success_url(self):
        investment_product_id = self.kwargs.get('investment_product_id') or self.get_object().investment_product.id
        return reverse_lazy('administrator:investment-product-detail', kwargs={'pk': investment_product_id})


class InvestmentCreateView(InvestmentMixin, CreateView):
    page_title = "Create Investment"

    def get_initial(self):
        initial = super().get_initial()
        initial = set_initial_value_field(initial, 'investment_product', self.kwargs.get('investment_product_id'))
        initial = set_initial_value_field(initial, 'user', self.kwargs.get('user_id'))
        return initial


class InvestmentUpdateView(InvestmentMixin, UpdateView):
    page_title = "Update Investment"


class InvestmentDeleteView(InvestmentMixin, DeleteView):
    page_title = "Delete Investment"
    template_name = 'administrator/base_confirm_delete.html'


class InvestmentDetailView(InvestmentMixin, DetailView):
    page_title = "Investment Info."
    template_name = 'administrator/investment_detail.html'
    context_object_name = "investment"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        investment = self.object
        stage_list = get_investment_stage_list(investment)
        contracts = [
            self._make_investment_contract_context(contract)
            for contract in InvestmentContract.objects.filter(investment=investment)
        ]
        context.update(
            stage_list=stage_list,
            contracts=contracts
        )
        return context


class InvestmentStepMixin(InvestmentMixin):
    model = InvestmentStep
    form_class = InvestmentStepForm
    context_object_name = "step"

    def get_success_url(self):
        return reverse_lazy(
            'administrator:investment-detail',
            kwargs={'pk': self.object.investment.id}
        )

    def get_initial(self):
        initial = super().get_initial()
        initial = set_initial_value_field(initial, 'investment', self.kwargs.get('investment_id'))
        initial = set_initial_value_field(initial, 'stage_id', self.kwargs.get('stage_id'))
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        investment_id = self.kwargs.get('investment_id')
        context['investment'] = get_object_or_404(Investment, id=investment_id)\
            if investment_id else self.object.investment
        return context


class InvestmentStepCreateView(InvestmentStepMixin, CreateView):
    page_title = "Create Investment Step"
    template_name = 'administrator/investment_step_form.html'


class InvestmentStepUpdateView(InvestmentStepMixin, UpdateView):
    page_title = "Update Investment Step"
    template_name = 'administrator/investment_step_form.html'


class InvestmentStepDeleteView(InvestmentStepMixin, DeleteView):
    page_title = "Delete Investment Step"
    template_name = 'administrator/base_confirm_delete.html'


class InvestmentStepEmailView(InvestmentStepMixin, DetailView):
    page_title = "Send Investment Step Email"
    template_name = 'administrator/investment_step_email.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        step = self.object
        email_template = 'email/investment_step.html'
        email_data = get_investment_step_email_data(self.request, step)
        context.update(
            email_template=email_template,
            email_contents=render_to_string('email/investment_step.html', email_data)
        )
        return context


# INVESTMENT PRODUCT
class InvestmentProductMixin(InvestmentMixin):
    model = InvestmentProduct
    form_class = InvestmentProductForm
    success_url = reverse_lazy('administrator:investment-product-list')


class InvestmentProductListView(InvestmentProductMixin, ListView):
    page_title = "Investment Products"
    template_name = "administrator/investment_product_list.html"
    context_object_name = "all_investment_product"
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_investment_product = context['all_investment_product']
        context['investment_product_list'] = [
            self._make_investment_product_context(investment_product)
            for investment_product in all_investment_product.all()
        ]
        return context


class InvestmentProductDetailView(InvestmentProductMixin, ManagementContext, DetailView):
    page_title = "Investment Product Info."
    template_name = "administrator/investment_product_detail.html"
    context_object_name = "investment_product"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        investment_product = context['investment_product']
        context['investment_product'] = self._make_investment_product_context(investment_product)
        context['investments'] = [
            InvestmentModel(
                id=investment.id,
                amount=safe_money_read_from_db(investment.amount),
                investor=self._make_investor_context(investment.user),
                investment_product=context['investment_product'],
            )
            for investment in investment_product.investments.all()
        ]
        # Product
        context['products'] = [
            self._make_product_context(product)
            for product in investment_product.product_set.all()
        ]
        context['connectable_products'] = Product.objects.exclude(
            investment_product=investment_product
        )
        context['investable_users'] = User.objects.exclude(
            investor_investments__investment_product=investment_product
        )

        return context


class InvestmentProductCreateView(InvestmentProductMixin, CreateView):
    page_title = "Create Investment Product"
    template_name = 'administrator/investment_product_form.html'


class InvestmentProductUpdateView(InvestmentProductMixin, UpdateView):
    page_title = "Update Investment Product"
    template_name = 'administrator/investment_product_form.html'


class InvestmentProductDeleteView(InvestmentProductMixin, DeleteView):
    page_title = "Delete Investment Product"
    template_name = 'administrator/base_confirm_delete.html'


# INVESTOR
class InvestorBaseView(InvestmentMixin):
    model = User
    success_url = reverse_lazy('administrator:investor-list')


class InvestorListView(InvestorBaseView, ListView):
    page_title = "Investors"
    template_name = "administrator/investor_list.html"
    context_object_name = "investor_list"
    paginate_by = 50

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['investors'] = [
            self._make_investor_context(investor)
            for investor in context['investor_list'].all()
        ]
        return context


class InvestorDetailView(InvestorBaseView, DetailView):
    page_title = "Investor Info."
    template_name = "administrator/investor_detail.html"
    context_object_name = "investor"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        investor = context['investor']
        context['investor'] = self._make_investor_context(investor)
        context['investments'] = [
            InvestmentModel(
                id=investment.id,
                amount=safe_money_read_from_db(investment.amount),
                investor=context['investor'],
                investment_product=self._make_investment_product_context(investment.investment_product),
            )
            for investment in investor.investor_investments.all()
        ]
        context['contracts'] = [
            self._make_investment_contract_context(contract)
            for contract in InvestmentContract.objects.filter(investment__user=investor)
        ]
        return context


# CONTRACT
class InvestmentContractMixin(InvestmentMixin):
    model = InvestmentContract
    form_class = InvestmentContractForm
    success_url = reverse_lazy('administrator:investment-product-list')

    def get_success_url(self):
        investment_id = self.kwargs.get('investment_id') if hasattr(self, 'kwargs') else None
        return reverse_lazy(
            'administrator:investment-detail',
            kwargs={'pk': self.object.investment.id}
        ) if investment_id else self.success_url


# TODO: 계약 플로우에 맞는 Template 호출
class InvestmentContractTemplateSelectView(InvestmentContractMixin, ListView):
    model = ContractTemplate
    page_title = "Investment Document Templates"
    template_name = 'administrator/investment_contract_template_select.html'
    context_object_name = "templates"
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        investment_id = self.kwargs['investment_id']

        templates = context[self.context_object_name]
        contracts = InvestmentContract.objects.filter(
            investment__id=investment_id,
            template__in=templates
        )
        for template in templates:
            template.issued = contracts.filter(template=template).count()
        context[self.context_object_name] = templates
        context['investment_id'] = investment_id
        return context


class InvestmentContractCreateView(InvestmentContractMixin, CreateView):
    page_title = "Create Investment Document"
    template_name = 'administrator/contract_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.kwargs.get('template_id'):
            context['template'] = get_object_or_404(ContractTemplate, id=self.kwargs['template_id'])
        investment = get_object_or_404(Investment, id=self.kwargs['investment_id'])
        contracts = InvestmentContract.objects.filter(investment=investment)
        context.update(
            investment=investment,
            contracts=contracts,
        )
        return context

    def form_valid(self, form):
        contract_form = form.save(commit=False)
        investment = get_object_or_404(Investment, id=self.kwargs['investment_id'])
        contract_form.investment = investment
        template = ContractTemplate.objects.get(
            id=self.kwargs['template_id']
        ) if self.kwargs.get('template_id') else None
        contract_form.template = template

        # E-signature
        if template and template.type == SIGNATURE:
            try:
                envelope_result = envelope_create(investment, template)
            except ApiException as e:
                err = json.loads(e.body)
                logger.error(f'Error has occurred while creating esignature envelope: {str(err)}')
                messages.warning(self.request, err.get('message'))
                return self.form_invalid(form)
            except Exception as e:
                logger.error(f'Error has occurred while creating esignature envelope: {str(e)}')
                messages.warning(self.request, "Creating contract failed. Please try again.")
                return self.form_invalid(form)
            else:
                logger.info(f'Esignature envelope created: {envelope_result}')
                contract_form.identifier = envelope_result.envelope_id

        db_update(contract_form)
        messages.success(self.request, "Contract Created")

        return super().form_valid(form)


class InvestmentContractUpdateView(InvestmentContractMixin, UpdateView):
    page_title = "Update Investment Document"
    template_name = 'administrator/contract_form.html'
    context_object_name = "contract"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        contract = context['contract']
        context.update(
            template=contract.template,
            investment=contract.investment,
        )
        return context


class InvestmentContractDeleteView(InvestmentContractMixin, DeleteView):
    page_title = "Delete Investment Document"
    template_name = 'administrator/base_confirm_delete.html'


# CONTRACT TEMPLATE
class ContractTemplateMixin(InvestmentMixin):
    model = ContractTemplate
    form_class = ContractTemplateForm

    def get_success_url(self):
        return reverse_lazy('administrator:contract-template-list')


class ContractTemplateListView(ContractTemplateMixin, ListView):
    page_title = "DOCUMENT TEMPLATE LIST"
    template_name = 'administrator/contract_template_list.html'
    context_object_name = "templates"
    paginate_by = 20


class ContractTemplateCreateView(ContractTemplateMixin, CreateView):
    page_title = "CREATE DOCUMENT TEMPLATE"
    template_name = 'administrator/base_form.html'


class ContractTemplateUpdateView(ContractTemplateMixin, UpdateView):
    page_title = "UPDATE DOCUMENT TEMPLATE"
    template_name = 'administrator/base_form.html'


class ContractTemplateDeleteView(ContractTemplateMixin, DeleteView):
    page_title = "DELETE DOCUMENT TEMPLATE"
    template_name = 'administrator/base_confirm_delete.html'
