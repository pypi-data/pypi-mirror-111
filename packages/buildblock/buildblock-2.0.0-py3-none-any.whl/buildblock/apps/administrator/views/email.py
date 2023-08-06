import logging

from django.contrib import messages
from django.shortcuts import redirect, render
from django.utils.translation import ugettext_lazy as _

from buildblock.apps.administrator.views.base import AdministratorServiceMixin, AdministratorTemplateView
from buildblock.apps.core.views import ListView
from buildblock.apps.users.models import User
from buildblock.services.email import EmailService

logger = logging.getLogger(__name__)


def administrator_send_message(request):
    request_info = request.POST
    email_title = request_info.get('email_title')
    email_message = request_info.get('email_message')
    recipients_list = request_info.getlist('email_recipient')
    logger.info(f'(recipients_list : {recipients_list}')

    result = EmailService.send_admin_email_to_group(
        recipients=recipients_list,
        title=email_title,
        message=email_message,
    )
    if result:
        messages.success(request, _('Email has successfully been sent.'))
        return redirect('administrator:email')
    else:
        messages.error(request, _('Sending Email failed.'))
        return redirect('administrator:email-message')


class EmailTargetListView(AdministratorServiceMixin, ListView):
    model = User
    context_object_name = "target_select_list"
    paginate_by = 50


class EmailWriteView(AdministratorTemplateView):
    template_name = "administrator/email_message.html"

    def post(self, request, **kwargs):
        request_info = request.POST
        email_group = request_info.get('target_group')

        recipients_list = User.objects.all()
        recipient_title = "All User"

        if email_group == 'Send To Owners':
            recipients_list = recipients_list.filter(user_role__contains=['owner_role'])
            recipient_title = "Owners"
        elif email_group == 'Send To Tenants':
            recipients_list = recipients_list.filter(user_role__contains=['tenant_role'])
            recipient_title = "Tenants"
        elif email_group == 'Send To Constructors':
            recipients_list = recipients_list.filter(user_role__contains=['constructor_role'])
            recipient_title = "Constructors"
        elif email_group == 'Send To Checked People':
            email_target_selected = request_info.getlist('target_select_input')
            recipients_list = recipients_list.filter(id__in=email_target_selected)
            recipient_title_list = []
            for recipient in recipients_list:
                recipient_title_list.append(recipient.name + " <" + recipient.email + ">")
            recipient_title = ', '.join(recipient_title_list)

        if not recipients_list:
            messages.error(request, _('Select the recipients.'))
            return redirect('administrator:email')

        context = {
            'recipient_title': recipient_title,
            'recipients': recipients_list,
        }

        return render(request, self.template_name, context)
