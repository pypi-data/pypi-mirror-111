from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.urls import reverse

from buildblock.apps.construction.contexts import ConstructionContext
from buildblock.apps.construction.forms import ConstructionForm, ConstructionUpdateForm
from buildblock.apps.construction.models import Construction
from buildblock.apps.core import views
from buildblock.apps.core.constants import COMPLETE, IN_PROGRESS, PENDING


class ConstructionServiceMixin(LoginRequiredMixin, ConstructionContext):
    model = Construction
    page_title = "CONSTRUCTION INFO"
    template_name = 'construction/construction_detail.html'
    ordering = ['-created_at']
    context_object_name = "construction"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        if self.kwargs.get('construction_id'):
            construction = get_object_or_404(Construction, id=self.kwargs['construction_id'])
            context['construction'] = self._make_construction_context(construction)

            # 권한
            is_editor = user.is_superuser or user in construction.constructor.all()
            if not is_editor and user not in construction.product.owner.all():
                raise PermissionDenied()
            context['is_editor'] = is_editor
        else:
            if user.is_superuser:
                constructions = Construction.objects.all()
            else:
                constructions = Construction.objects.filter(
                    Q(product__owner=user) | Q(constructor=user)
                ).distinct()

            # Order by
            constructions = constructions.order_by('-created_at')

            # Status Filter
            # 아래 List 안에 순서대로 출력됩니다.
            construction_status_list = [IN_PROGRESS, PENDING, COMPLETE]
            if self.request.GET.get('status') in construction_status_list:
                constructions = constructions.filter(
                    status=self.request.GET.get('status')
                )
            else:
                constructions_sorted = list()
                for status in construction_status_list:
                    constructions_sorted.extend(constructions.filter(status=status))
                constructions = constructions_sorted

            context['constructions'] = self._make_all_constructions_context(constructions)

        return context

    def get_success_url(self):
        construction_id = self.kwargs.get('construction_id') or self.kwargs.get('pk')
        if construction_id:
            return reverse('construction:info', kwargs={'construction_id': construction_id})
        return reverse('construction:home')


class ConstructionTemplateView(ConstructionServiceMixin, views.TemplateView):
    pass


class ConstructionDetailView(ConstructionServiceMixin, views.DetailView):
    pass


class ConstructionListView(ConstructionServiceMixin, views.ListView):
    template_name = "construction/construction_list.html"
    page_title = "CONSTRUCTION LIST"
    paginate_by = 20


class ConstructionFormView(ConstructionServiceMixin):
    form_class = ConstructionForm
    template_name = 'construction/construction_form.html'


class ConstructionCreateView(ConstructionFormView, views.CreateView):
    page_title = "CREATE CONSTRUCTION"


class ConstructionUpdateView(ConstructionFormView, views.UpdateView):
    page_title = "UPDATE CONSTRUCTION"
    form_class = ConstructionUpdateForm
    template_name = 'construction/construction_update_form.html'


class ConstructionDeleteView(ConstructionFormView, views.DeleteView):
    page_title = "DELETE CONSTRUCTION"
    template_name = 'construction/construction_delete.html'
