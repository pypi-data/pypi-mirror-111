from django.urls import reverse_lazy

from buildblock.apps.administrator.forms import ProductForm
from buildblock.apps.administrator.views.base import AdministratorServiceMixin
from buildblock.apps.construction.contexts import ConstructionContext
from buildblock.apps.core.views import CreateView, DeleteView, DetailView, ListView, UpdateView
from buildblock.apps.investment.contexts import InvestmentContext
from buildblock.apps.management.contexts import ManagementContext
from buildblock.apps.product.models import Product


class AdministratorProductBaseView(
    AdministratorServiceMixin,
    ManagementContext,
    ConstructionContext,
    InvestmentContext
):
    model = Product
    page_title = "Product"
    context_object_name = "product"
    form_class = ProductForm
    template_name = "administrator/base_form.html"
    success_url = reverse_lazy('administrator:product-list')


class AdministratorProductListView(AdministratorProductBaseView, ListView):
    context_object_name = "products"
    template_name = "administrator/product_list.html"
    page_title = "Products"
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = context[self.context_object_name]
        context[self.context_object_name] = [
            self._make_product_context(product)
            for product in products
        ]
        return context


class AdministratorProductDetailView(AdministratorProductBaseView, DetailView):
    template_name = "administrator/product_detail.html"
    page_title = "Product Info."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object
        context["product"] = self._make_product_context(product)
        if product.investment_product:
            context["investment_product"] = self._make_investment_product_context(
                investment_product=product.investment_product
            )
        if product.constructions:
            context["constructions"] = self._make_all_constructions_context(
                constructions=product.constructions.all()
            )
        return context


class AdministratorProductFormView(AdministratorProductBaseView):
    def get_success_url(self):
        return reverse_lazy('administrator:product-detail', kwargs={'pk': self.object.pk})


class AdministratorProductCreateView(AdministratorProductFormView, CreateView):
    page_title = "Create Product"


class AdministratorProductUpdateView(AdministratorProductFormView, UpdateView):
    page_title = "Update Product"


class AdministratorProductDeleteView(AdministratorProductBaseView, DeleteView):
    template_name = "administrator/base_confirm_delete.html"
    page_title = "Delete Product"
