from django.contrib import messages
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from buildblock.apps.administrator.forms import PropertyFilterCreateForm, PropertyFilterForm
from buildblock.apps.administrator.views.base import AdministratorServiceMixin
from buildblock.apps.core.views import DeleteView, FormView, ListView, TemplateView
from buildblock.apps.property.constants import PropertyCallEnum, PropertyInfoOriginEnum
from buildblock.apps.property.handlers.zillow import ZillowPropertyHandler
from buildblock.apps.property.models import PropertySubscriptionFilter
from buildblock.helper import db_update

PROPERTY_HANDLER_MAPPING = {
    PropertyInfoOriginEnum.ZILLOW.value: ZillowPropertyHandler,
}

FILTER_BASIC_INFO_KEY_SET = frozenset(['title', 'emails', 'id' 'status', 'messaging_template'])


def property_filter_data_set(data: dict):
    return {
        k: data[k] for k in data.keys()
        if k not in FILTER_BASIC_INFO_KEY_SET and data[k]
    }


class PropertyView(AdministratorServiceMixin):
    page_title = "Properties"
    form_class = PropertyFilterForm
    model = PropertySubscriptionFilter

    def dispatch(self, request, *args, **kwargs):
        self.info_origin = self.kwargs.get('info_origin', self.info_origin)
        self.property_handler = PROPERTY_HANDLER_MAPPING.get(self.info_origin)
        if not self.property_handler:
            raise Http404
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('administrator:property-sale-list')


class PropertyListView(PropertyView, FormView):
    template_name = "administrator/property_list.html"

    def form_valid(self, form):
        context = self.get_context_data()
        handler = self.property_handler(
            type=self.list_type,
            data=dict(form.cleaned_data)
        )
        update_data = handler.run()
        context.update(update_data)
        return self.render_to_response(context)

    @property
    def list_type(self):
        raise NotImplementedError


class PropertySaleListView(PropertyListView):
    page_title = "Sale Properties"
    list_type = PropertyCallEnum.PROPERTY_SALE_LIST


class PropertySoldListView(PropertyListView):
    page_title = "Sold Properties"
    list_type = PropertyCallEnum.PROPERTY_SOLD_LIST


class PropertyDetailView(PropertyView, TemplateView):
    page_title = "Property Info."
    template_name = "administrator/property_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        property_id = self.kwargs.get('property_id')
        if not property_id:
            messages.error(self.request, 'The Property ID does not exist. Please try again.')
            return context
        handler = self.property_handler(
            type=PropertyCallEnum.PROPERTY_DETAIL,
            data=dict(property_id=property_id)
        )
        update_data = handler.run()
        context.update(update_data)
        return context


class PropertyFilterListView(PropertyView, ListView):
    page_title = "Property Filters"
    template_name = "administrator/property_filter_list.html"
    context_object_name = "filters"
    paginate_by = 20
    ordering = ['-modified_at']


class PropertyFilterFormView(PropertyView, FormView):
    template_name = "administrator/base_form.html"
    form_class = PropertyFilterCreateForm
    success_msg = _('Filter registered successfully.')
    error_msg = _('Filter registration failed. Please, try again.')

    def get_success_url(self):
        if hasattr(self, 'filter_object'):
            return reverse_lazy(
                'administrator:property-filter-update',
                kwargs={'info_origin': self.info_origin,
                        'filter_id': self.filter_object.id}
            )
        return reverse_lazy(
            'administrator:property-filter-list',
            kwargs={'info_origin': self.info_origin}
        )

    def get_initial(self):
        initial = self.initial.copy()
        filter_id = self.kwargs.get('filter_id')
        self.filter_object = get_object_or_404(
            PropertySubscriptionFilter,
            pk=filter_id
        ) if filter_id else PropertySubscriptionFilter()
        if self.filter_object:
            initial.update(self.filter_object.__dict__)
            initial.update(self.filter_object.filter)
            initial.update(messaging_template=self.filter_object.messaging_template)
        return initial

    def form_valid(self, form):
        context = self.get_context_data()
        data_dict = dict(
            title=form.cleaned_data['title'],
            emails=form.cleaned_data['emails'],
            status=form.cleaned_data['status'],
            messaging_template=form.cleaned_data['messaging_template'],
            filter=property_filter_data_set(form.cleaned_data)
        )
        if db_update(self.filter_object, data_dict):
            messages.success(self.request, self.success_msg)
            return HttpResponseRedirect(self.get_success_url())
        else:
            messages.error(self.request, self.error_msg)
            return self.render_to_response(context)


class PropertyFilterCreateView(PropertyFilterFormView):
    page_title = "Create Property Filter"


class PropertyFilterUpdateView(PropertyFilterFormView):
    page_title = "Update Property Filter"
    success_msg = _('The filter updated successfully.')
    error_msg = _('The filter update failed. Please, try again.')


class PropertyFilterDeleteView(PropertyView, DeleteView):
    page_title = "Delete Property Filter"
    template_name = "base_confirm_delete.html"
