import logging

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _

from buildblock.apps.access_control import require_admin_access
from buildblock.apps.core.views import ListView, TemplateView
from buildblock.apps.messaging.forms import MessagingCreateValForm, MessagingSendValForm
from buildblock.apps.messaging.models import MessagingTemplates
from buildblock.apps.users.models import User
from buildblock.services.aws import AwsService
from buildblock.services.messaging import MessagingService

logger = logging.getLogger(__name__)


def messaging_upsert(request):
    form = MessagingCreateValForm(request.POST)
    if not form.is_valid():
        messages.warning(request,
                         _("You have entered an invalid information. Please try again."))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    creator = request.user
    title = form.cleaned_data.get('title')
    category = form.cleaned_data.get('category')
    is_active = form.cleaned_data.get('is_active')
    content = request.POST.get('content')
    description = form.cleaned_data.get('description')

    template_id = request.POST.get('template_id')
    if template_id:
        MessagingService.edit_messaging_template(
            template_id=template_id,
            title=title,
            category=category,
            is_active=is_active,
            description=description
        )
    else:
        template = MessagingService.add_messaging_template(
            creator_id=creator.id,
            title=title,
            category=category,
            is_active=is_active,
            description=description
        )
        template_id = template.id

    success = AwsService.put_messaging_template(template_id, content)
    if success:
        messages.success(request, _("Messaging template has successfully been uploaded."))
        return redirect('messaging:template-list')
    return messages.warning(request, _("Uploading messaging template failed."))


def messaging_send(request):
    form = MessagingSendValForm(request.POST)
    if not form.is_valid():
        messages.warning(request,
                         _("You have entered an invalid information. Please try again."))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    title = form.cleaned_data.get('message_title')
    content = request.POST.get('message_content')
    # TODO 여러명에게 보낼 수 있는 기능 추가
    receiver_id = form.cleaned_data.get('receiver_id')
    try:
        receiver = User.objects.get(id=receiver_id)
    except Exception as e:
        logger.info(f'Recipient(id:{receiver.id}) does not exist: ' + e)
        return messages.warning(request, _("Recipient does not exist."))

    # TODO 일단 admin이 발송인 (현재 buildblock.io로 끝나는 메일은 모두 발송인이 될 수 있음)
    success = MessagingService.send_message(title, content, [receiver.email])
    if success:
        messages.success(request, _("Email has successfully been sent to ") + receiver.name)
        return redirect('messaging:template-list')
    return messages.warning(request, _("Sending Email failed."))


class MessagingBaseView(LoginRequiredMixin):
    page_title = "Messaging Page"

    @require_admin_access
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.page_title
        return context


class MessagingView(MessagingBaseView, TemplateView):
    pass


class MessagingListView(MessagingBaseView, ListView):
    page_title = "Messaging Templates"
    model = MessagingTemplates
    context_object_name = "templates"
    template_name = "messaging/index.html"
    ordering = ['-is_active', '-created_at']


class MessagingFormView(MessagingBaseView, TemplateView):
    template_name = "messaging/template-form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        template_id = self.kwargs.get('pk')
        if template_id:
            context['page_title'] = "Edit Messaging Template"
            context['template'] = MessagingService.get_messaging_template(template_id)
            context['template_content'] = AwsService.get_messaging_template(template_id)
        else:
            context['page_title'] = "Create Messaging Template"

        return context


class MessagingSendView(MessagingBaseView, TemplateView):
    page_title = "Send Message"
    template_name = "messaging/message-form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        template_id = self.kwargs.get('pk')
        context['template'] = MessagingService.get_messaging_template(template_id)
        context['template_content'] = AwsService.get_messaging_template(template_id)
        # TODO: 발송인 정리해야함 (staff 권한을 가진 모든 사람을 목록으로 뿌릴지 아님 공식 메일 몇 개를 정해서 고르게 할지)
        context['sender_list'] = User.objects.filter(is_staff=True)
        context['receiver_list'] = User.objects.all()

        return context
