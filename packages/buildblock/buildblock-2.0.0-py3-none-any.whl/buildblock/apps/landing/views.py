import logging
from datetime import date

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.utils.translation import get_language
from django.utils.translation import ugettext_lazy as _

from buildblock.apps.administrator.models import Faq
from buildblock.apps.core import views
from buildblock.apps.core.constants import AFTER, BEFORE, ENGLISH
from buildblock.apps.core.enums import TeamMemberDepartment
from buildblock.apps.landing.constants import (
    ACTIVE,
    BLOG,
    CAREER,
    COMPLETE,
    EVENT,
    INTERVIEW,
    NEWS,
    NOTICE,
    OPEN,
    PENDING
)
from buildblock.apps.landing.forms import CaseStudyForm, ContactEmailForm, NewsForm
from buildblock.apps.landing.models import (
    CaseStudy,
    History,
    LandingCarousel,
    LandingDocument,
    LandingInformation,
    LandingPopup,
    LandingThinBanner,
    LandingVideo,
    News,
    Team
)
from buildblock.services.email import EmailService

logger = logging.getLogger(__name__)

_MAX_LANDING_CASE_STUDY_LIST_SIZE = 4


class LandingViewMixin:
    def get_context_data(self, **kwargs):
        # self.object_list = self.get_queryset()
        context = super().get_context_data(**kwargs)
        language = get_language()
        today = date.today()
        all_information = LandingInformation.objects.all()
        landing_information = all_information.filter(language=language).first()
        if not landing_information:
            landing_information = all_information.filter(language=ENGLISH).first()
        context['information'] = landing_information

        context['landing_thin_banner'] = LandingThinBanner.objects.filter(
            start_date__lte=today,
            end_date__gte=today,
            is_active=True
        ).first()

        return context


class LandingHomeView(LandingViewMixin, views.TemplateView):
    template_name = "landing/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        language = get_language()
        today = date.today()
        context['landing_popup'] = LandingPopup.objects.filter(
            start_date__lte=today,
            end_date__gte=today,
            is_active=True
        ).first()
        context['active_carousel'] = LandingCarousel.objects.filter(
            start_date__lte=today,
            end_date__gte=today,
            is_active=True
        ).order_by('ordering')

        context['landing_case_study_list'] = CaseStudy.objects.filter(
            language=language,
            headline=True,
            is_private=False
        ).order_by('-status')[:_MAX_LANDING_CASE_STUDY_LIST_SIZE]

        context['landing_video_list'] = LandingVideo.objects.all().order_by('ordering')

        return context


class LandingAboutView(LandingViewMixin, views.TemplateView):
    page_title = _("About Company")
    template_name = "landing/about.html"


class LandingHistoryView(LandingViewMixin, views.TemplateView):
    page_title = _("History")
    template_name = "landing/history.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        all_history = History.objects.all()
        history_group = []
        for history in all_history.distinct("year", "quarter"):
            data_list = {
                'date_display': history.date_display,
                'content_by_date': all_history.filter(
                    year=history.year,
                    quarter=history.quarter
                ).order_by("ordering")
            }
            history_group.append(data_list)
        context['history_group'] = history_group

        all_team = Team.objects.all()
        team_group = []
        for department in TeamMemberDepartment:
            data_list = {
                'department': department.value,
                'members': all_team.filter(
                    department=department.name
                ).order_by("ordering")
            }
            team_group.append(data_list)
        context['team_group'] = team_group

        return context


class LandingServiceView(LandingViewMixin, views.TemplateView):
    page_title = _("Service")


class CaseStudyListView(LandingViewMixin, views.ListView):
    model = CaseStudy
    page_title = _("Invest")
    template_name = "landing/case_study_list.html"
    paginate_by = 12
    context_object_name = "case_studies"
    ordering = ['-report_date']

    def get_queryset(self):
        queryset = super().get_queryset()
        # Language Filter
        language = get_language()
        queryset = queryset.filter(is_private=False, language=language)
        # Ordering by Status
        _status_list = [OPEN, PENDING, ACTIVE, COMPLETE]
        return sorted(
            queryset.filter(status__in=_status_list),
            key=lambda x: _status_list.index(x.status)
        )


class CaseStudyCreateView(LandingViewMixin, views.CreateView):
    model = CaseStudy
    form_class = CaseStudyForm
    template_name = "landing/case_study_write.html"

    def get_success_url(self):
        return reverse('case-study-read', kwargs={'pk': self.object.pk})


class CaseStudyDetailView(LandingViewMixin, views.HitCountDetailView):
    model = CaseStudy
    template_name = "landing/case_study_read.html"
    context_object_name = "case_study"
    count_hit = True

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        case_study_photos = self.object.photos
        context['before_photos'] = case_study_photos.filter(status=BEFORE)
        context['after_photos'] = case_study_photos.filter(status=AFTER)
        context['videos'] = self.object.videos.all()
        return context


class CaseStudyUpdateView(LandingViewMixin, views.UpdateView):
    model = CaseStudy
    form_class = CaseStudyForm
    template_name = "landing/case_study_write.html"

    def get_success_url(self):
        return reverse('case-study-read', kwargs={'pk': self.object.pk})


class CaseStudyDeleteView(LandingViewMixin, views.DeleteView):
    model = CaseStudy
    template_name = 'landing/case_study_delete.html'
    success_url = reverse_lazy('case-study')


class CareerListView(LandingViewMixin, views.ListView):
    model = News
    page_title = _("Career")
    template_name = "landing/career.html"
    context_object_name = "news_list"

    def get_queryset(self):
        queryset = super().get_queryset()
        language = get_language()
        return queryset.filter(
            news_category__in=[CAREER],
            language=language
        ).order_by('-report_date')


class NewsBaseView(LandingViewMixin):
    model = News
    page_title = _("News")


class NewsListView(NewsBaseView, views.ListView):
    template_name = "landing/news_list.html"
    paginate_by = 9
    context_object_name = "news_list"
    ordering = ['-report_date']

    def get_queryset(self):
        queryset = super().get_queryset()
        language = get_language()

        queryset = queryset.filter(
            news_category__in=[NEWS, BLOG, NOTICE, EVENT, INTERVIEW],
            language=language
        )

        return queryset


class NewsCreateView(NewsBaseView, views.CreateView):
    form_class = NewsForm
    template_name = "landing/news_write.html"

    def get_success_url(self):
        return reverse('news-read', kwargs={'pk': self.object.pk})


class NewsDetailView(NewsBaseView, views.HitCountDetailView):
    template_name = "landing/news_read.html"
    context_object_name = "news"
    count_hit = True

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        list_url = 'career' if self.object.news_category == CAREER else 'news'
        context['list_url'] = reverse_lazy(list_url)
        return context


class NewsUpdateView(NewsBaseView, views.UpdateView):
    form_class = NewsForm
    template_name = "landing/news_write.html"

    def get_success_url(self):
        return reverse('news-read', kwargs={'pk': self.object.pk})


class NewsDeleteView(NewsBaseView, views.DeleteView):
    template_name = 'landing/news_delete.html'
    success_url = reverse_lazy('news')


class ContactView(LandingViewMixin, views.FormView):
    page_title = _("Contact")
    template_name = "landing/contact.html"
    form_class = ContactEmailForm

    def form_valid(self, form):
        return_url = self.request.META.get('HTTP_REFERER')
        EmailService.send_contact_email_to_help(
            name=form.cleaned_data['name'],
            phone=form.cleaned_data['phone'],
            email=form.cleaned_data['email'],
            content=form.cleaned_data['message'],
        )
        messages.success(self.request, _('Email has successfully been sent.'))
        return HttpResponseRedirect(return_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        language = get_language()
        context['landing_document'] = LandingDocument.objects.filter(language=language)
        context['faq_list'] = Faq.objects.filter(language=language).order_by('num')

        return context
