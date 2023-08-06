import logging
from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from buildblock.apps.core.constants import (
    AGENT_ROLE,
    COMMENT_ADD,
    COMMENT_DELETE,
    CREATED,
    DONE,
    MAINTENANCE_STATUS_LIST,
    OWNER_ROLE,
    PENDING,
    STATUS_CHANGE,
    TENANT_ROLE
)
from buildblock.apps.management.forms import MaintenanceCreateForm, MaintenanceUpdateForm
from buildblock.apps.management.models import Lease, Maintenance
from buildblock.apps.management.views.base import (
    ManagementCreateView,
    ManagementDetailView,
    ManagementListView,
    ManagementUpdateView
)
from buildblock.apps.view_control import is_valid_post_request
from buildblock.helper import db_update
from buildblock.services.email import EmailService

logger = logging.getLogger(__name__)

MAINTENANCE_STATUS_CHANGEABLE_ROLE_LIST = frozenset([OWNER_ROLE, AGENT_ROLE])


def _has_maintenance_permission(product, user):
    return bool(
        user in product.owner.all()
        or Lease.objects.filter(product=product, tenant=user)
        or product.agency in user.groups.all()
    )


@login_required
def maintenance_status_change(request):
    if not is_valid_post_request(request):
        return redirect('maintenance:home')

    # Maintenance Check
    try:
        maintenance_id = request.POST.get('maintenance_id')
        maintenance = Maintenance.objects.get(id=maintenance_id)
    except Maintenance.DoesNotExist:
        messages.warning(request, _("The maintenance request doesn't exist."))
        return redirect(reverse("management:maintenance"))

    # Change rights check
    if request.session['active_role'] not in MAINTENANCE_STATUS_CHANGEABLE_ROLE_LIST \
       or not _has_maintenance_permission(product=maintenance.product, user=request.user):
        messages.warning(request, _("You don't have permission to modify this maintenance request status."))
        return redirect(reverse("management:maintenance"))

    # Status Check
    try:
        # TODO: 일단 두가지 상태
        status = PENDING if maintenance.status == DONE else DONE
        db_update(maintenance, dict(status=status))
        messages.success(request, _("The maintenance request status is changed successfully."))

        # Email Alert
        EmailService._send_emails_for_maintenace_event_type(
            maintenance=maintenance,
            request_user=request.user,
            event_type=STATUS_CHANGE,
        )
    except Exception as e:
        logger.error(f'Error while change resolved status: {str(e)}')
        messages.warning(request, _('Please try again.'))

    return redirect("management:maintenance-read", pk=maintenance_id)


@login_required
def maintenance_comment_add(request):
    if not is_valid_post_request(request):
        return redirect("maintenance:home")

    # Maintenance Check
    try:
        maintenance_id = request.POST.get('maintenance_id')
        maintenance = Maintenance.objects.get(id=maintenance_id)
    except Maintenance.DoesNotExist:
        messages.warning(request, _("The maintenance request doesn't exist."))
        return redirect(reverse("management:maintenance"))

    # Change rights check
    if not _has_maintenance_permission(product=maintenance.product, user=request.user):
        messages.warning(request, _("You don't have permission."))
        return redirect(reverse("management:maintenance"))

    # Data Check & comment add
    comment_content = request.POST.get('comment_content')
    if len(comment_content.replace(" ", "")) < 1:
        messages.error(request, _("Please enter the contents."))
    else:
        try:
            created_time = str(datetime.utcnow().timestamp())
            maintenance.comments[created_time] = {
                "writer": request.user.id,
                "content": comment_content
            }
            db_update(maintenance)
            messages.success(request, _("A new comment is registered successfully."))

            # Email Alert
            EmailService._send_emails_for_maintenace_event_type(
                maintenance=maintenance,
                request_user=request.user,
                event_type=COMMENT_ADD,
                comment=comment_content,
            )
        except Exception as e:
            logger.error(f'Error while comment add: {str(e)}')
            messages.warning(request, _("Please try again."))

    return redirect("management:maintenance-read", pk=maintenance_id)


@login_required
def maintenance_comment_delete(request):
    if not is_valid_post_request(request):
        return redirect("maintenance:home")

    # Maintenance Check
    try:
        comment_created_at = request.POST.get('comment_created_at')
        maintenance_id = request.POST.get('maintenance_id')
        maintenance = Maintenance.objects.get(id=maintenance_id)
    except Maintenance.DoesNotExist:
        messages.warning(request, _("The maintenance request doesn't exist."))
        return redirect(reverse("management:maintenance"))

    # Comment exist check & delete
    comment = maintenance.comments.get(comment_created_at, None)
    if not comment:
        messages.warning(request, _("This comment doesn't exist"))
    elif comment["writer"] != request.user.id:
        messages.warning(request, _("You don't have permission."))
    else:
        try:
            maintenance.comments.pop(comment_created_at)
            db_update(maintenance)
            messages.success(request, _("The comment is deleted successfully."))

            # Email Alert
            EmailService._send_emails_for_maintenace_event_type(
                maintenance=maintenance,
                request_user=request.user,
                event_type=COMMENT_DELETE,
            )
        except Exception as e:
            logger.error(f'Error while comment delete: {str(e)}')
            messages.error(request, _("Please try again."))

    return redirect("management:maintenance-read", pk=maintenance_id)


class ManagementMaintenanceListView(ManagementListView):
    model = Maintenance
    template_name = "management/maintenance.html"
    paginate_by = 10
    context_object_name = "maintenances"

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.active_role == TENANT_ROLE:
            queryset = queryset.filter(tenant=self.request.user)
        else:
            queryset = queryset.filter(product__in=self.products)

        # Status Filter
        if self.request.GET.get('status') in MAINTENANCE_STATUS_LIST:
            queryset = queryset.filter(
                status__in=MAINTENANCE_STATUS_LIST.get(self.request.GET.get('status'))
            )

        queryset = queryset.order_by('-created_at')
        return queryset


class ManagementMaintenanceDetailView(ManagementDetailView):
    model = Maintenance
    template_name = "management/maintenance-read.html"
    context_object_name = "maintenance"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        maintenance = self.object

        # permission check & read change
        if not _has_maintenance_permission(product=maintenance.product, user=self.request.user):
            messages.warning(self.request, _("You don't have permission"))
            return redirect(reverse("management:maintenance"))

        if self.active_role == OWNER_ROLE:
            db_update(maintenance, dict(is_read=True))

        context['product'] = self._make_product_context(maintenance.product)
        context['leases'] = self._make_all_leases_context(maintenance.product)
        context['maintenance_status_changeable_roles'] = MAINTENANCE_STATUS_CHANGEABLE_ROLE_LIST
        return context


class ManagementMaintenanceCreateView(ManagementCreateView):
    model = Maintenance
    form_class = MaintenanceCreateForm
    template_name = "management/maintenance-write.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Tenant
        if context.get('residence'):
            context['product'] = context['residence']['product']
            return context
        else:
            messages.warning(self.request, _('Invalid Access'))
            return redirect(reverse("management:maintenance"))

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['product'] = self.lease.product
        kwargs['tenant'] = self.lease.tenant
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, _('A new maintenance request is registered successfully.'))
        try:
            # Email Alert
            EmailService._send_emails_for_maintenace_event_type(
                maintenance=form.save(commit=False),
                request_user=self.request.user,
                event_type=CREATED,
            )
        except Exception as e:
            logger.error(f'Error while maintenance emailing: {str(e)}')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('management:maintenance-read', kwargs={'pk': self.object.pk})


class ManagementMaintenanceUpdateView(ManagementUpdateView):
    model = Maintenance
    form_class = MaintenanceUpdateForm
    template_name = "management/maintenance-write.html"
    context_object_name = "maintenance"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.tenant != self.request.user:
            messages.warning(self.request, _('Invalid Access'))
            return redirect(reverse("management:maintenance"))
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = self._make_product_context(context['maintenance'].product)
        return context

    def get_success_url(self):
        return reverse("management:maintenance-read", kwargs={'pk': self.object.pk})
