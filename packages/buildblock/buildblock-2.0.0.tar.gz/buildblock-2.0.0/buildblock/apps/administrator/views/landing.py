import logging

from django.http import JsonResponse
from django.urls import reverse_lazy

from buildblock.apps.administrator.forms import (
    CaseStudyForm,
    CaseStudyPhotoForm,
    CaseStudyVideoForm,
    FaqForm,
    HistoryForm,
    LandingCarouselForm,
    LandingDocumentForm,
    LandingInfoForm,
    LandingPopupForm,
    LandingThinBannerForm,
    LandingVideoForm,
    NewsForm,
    TeamForm
)
from buildblock.apps.administrator.models import Faq
from buildblock.apps.administrator.views.base import AdministratorServiceMixin
from buildblock.apps.core.constants import AFTER, BEFORE
from buildblock.apps.core.views import CreateView, DeleteView, ListView, UpdateView
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
from buildblock.services.administrator import LandingService
from buildblock.utils import json_error_response

logger = logging.getLogger(__name__)


DELETE_CASE_STUDY_MEDIA_MAPPING = {
    'video': LandingService.delete_case_study_video,
    'photo': LandingService.delete_case_study_photo
}


def create_case_study_video_ajax(request):
    if request.is_ajax:
        form = CaseStudyVideoForm(request.POST)
        if form.is_valid():
            new_form = form.save()
            data = {
                'id': new_form.id,
                'url': new_form.url,
            }
            return JsonResponse(data)

    return json_error_response("Error has occurred. Try again")


def create_case_study_photo_ajax(request):
    if request.is_ajax:
        form = CaseStudyPhotoForm(request.POST, request.FILES)
        if form.is_valid():
            new_form = form.save()
            data = {
                'id': new_form.id,
                'thumbnail': new_form.thumbnail_image_url,
            }
            return JsonResponse(data)

    return json_error_response("Error has occurred. Try again")


def delete_case_study_media_ajax(request):
    if request.is_ajax and request.method == "POST":
        media_type = request.POST.get('media_type')
        media_id = request.POST.get('media_id')
        delete_function = DELETE_CASE_STUDY_MEDIA_MAPPING[media_type]
        delete_function(media_id)

        data = {
            'media_type': media_type,
            'media_id': media_id,
        }
        return JsonResponse(data)

    return json_error_response("Error has occurred. Try again")


# Company Info.
class LandingInfoView(AdministratorServiceMixin):
    model = LandingInformation
    success_url = reverse_lazy('administrator:company-info-list')


class LandingInfoListView(LandingInfoView, ListView):
    page_title = "Company Info."
    template_name = "administrator/company_info.html"
    context_object_name = "company_info"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['landing_document'] = LandingDocument.objects.all()

        return context


class LandingInfoFormView(LandingInfoView):
    form_class = LandingInfoForm
    template_name = "administrator/base_form.html"


class LandingInfoCreateView(LandingInfoFormView, CreateView):
    page_title = "Add Information"


class LandingInfoUpdateView(LandingInfoFormView, UpdateView):
    page_title = "Update Information"


class LandingInfoDeleteView(LandingInfoView, DeleteView):
    page_title = "Delete Information"
    template_name = "administrator/base_confirm_delete.html"


class LandingDocumentFormView(LandingInfoView):
    model = LandingDocument
    form_class = LandingDocumentForm
    template_name = "administrator/base_form.html"
    success_url = reverse_lazy('administrator:company-info-list')


class LandingDocumentCreateView(LandingDocumentFormView, CreateView):
    page_title = "Add Document"


class LandingDocumentUpdateView(LandingDocumentFormView, UpdateView):
    page_title = "Update Document"


class LandingDocumentDeleteView(AdministratorServiceMixin, DeleteView):
    model = LandingDocument
    page_title = "Delete Document"
    template_name = "administrator/base_confirm_delete.html"
    success_url = reverse_lazy('administrator:company-info-list')


# History Management
class HistoryListView(AdministratorServiceMixin, ListView):
    model = History
    page_title = "Company History"
    template_name = "administrator/history_list.html"
    context_object_name = "history_list"
    ordering = ['-year', '-quarter', 'ordering']


class HistoryFormView(AdministratorServiceMixin):
    model = History
    success_url = reverse_lazy('administrator:history-list')


class HistoryCreateView(HistoryFormView, CreateView):
    page_title = "Create History"
    form_class = HistoryForm
    template_name = 'administrator/history_form.html'


class HistoryUpdateView(HistoryFormView, UpdateView):
    page_title = "Update History"
    form_class = HistoryForm
    template_name = 'administrator/history_form.html'


class HistoryDeleteView(HistoryFormView, DeleteView):
    page_title = "Delete History"
    template_name = 'administrator/history_confirm_delete.html'


# Team Member Management
class TeamListView(AdministratorServiceMixin, ListView):
    model = Team
    page_title = "Team"
    template_name = "administrator/team_list.html"
    context_object_name = "team_list"
    ordering = ['-created_at']
    paginate_by = 30


class TeamFormView(AdministratorServiceMixin):
    model = Team
    success_url = reverse_lazy('administrator:team-list')


class TeamCreateView(TeamFormView, CreateView):
    page_title = "Add Member"
    form_class = TeamForm
    template_name = 'administrator/team_form.html'


class TeamUpdateView(TeamFormView, UpdateView):
    page_title = "Update Member"
    form_class = TeamForm
    template_name = 'administrator/team_form.html'


class TeamDeleteView(TeamFormView, DeleteView):
    page_title = "Delete Member"
    template_name = 'administrator/team_confirm_delete.html'


# Case Study Post Management (=Invest)
class CaseStudyListView(AdministratorServiceMixin, ListView):
    model = CaseStudy
    page_title = "Case Study"
    template_name = "administrator/case_study_list.html"
    context_object_name = "case_study_list"
    ordering = ['-title', '-created_at']
    paginate_by = 18


class CaseStudyFormView(AdministratorServiceMixin):
    model = CaseStudy
    success_url = reverse_lazy('administrator:case-study-list')
    form_class = CaseStudyForm
    template_name = 'administrator/case_study_form.html'


class CaseStudyCreateView(CaseStudyFormView, CreateView):
    page_title = "Create Case Study"


class CaseStudyUpdateView(CaseStudyFormView, UpdateView):
    page_title = "Edit Case Study"
    context_object_name = "case_study"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        case_study = LandingService.get_case_study(self.kwargs.get('pk'))
        case_study_photos = case_study.photos.order_by('created_at')
        context['videos'] = case_study.videos.order_by('created_at')
        context['before_photos'] = case_study_photos.filter(status=BEFORE)
        context['after_photos'] = case_study_photos.filter(status=AFTER)

        return context


class CaseStudyDeleteView(AdministratorServiceMixin, DeleteView):
    page_title = "Delete Case Study"
    template_name = 'administrator/case_study_confirm_delete.html'
    model = CaseStudy
    success_url = reverse_lazy('administrator:case-study-list')


# News Management
class NewsListView(AdministratorServiceMixin, ListView):
    model = News
    page_title = "News"
    template_name = "administrator/news_list.html"
    context_object_name = "news_list"
    ordering = ['-report_date']
    paginate_by = 20


class NewsFormView(AdministratorServiceMixin):
    model = News
    success_url = reverse_lazy('administrator:news-list')


class NewsCreateView(NewsFormView, CreateView):
    page_title = "Write News"
    form_class = NewsForm
    template_name = 'administrator/news_form.html'


class NewsUpdateView(NewsFormView, UpdateView):
    page_title = "Edit News"
    form_class = NewsForm
    context_object_name = "news"
    template_name = 'administrator/news_form.html'


class NewsDeleteView(NewsFormView, DeleteView):
    page_title = "Delete News"
    template_name = 'administrator/news_confirm_delete.html'


# Landing Video (Youtube)
class LandingVideoView(AdministratorServiceMixin):
    model = LandingVideo
    success_url = reverse_lazy('administrator:landing-video-list')


class LandingVideoListView(LandingVideoView, ListView):
    page_title = "Landing Video"
    template_name = "administrator/landing_video_list.html"
    context_object_name = "landing_video"
    ordering = ['ordering']


class LandingVideoFormView(LandingVideoView):
    form_class = LandingVideoForm
    template_name = "administrator/base_form.html"


class LandingVideoCreateView(LandingVideoFormView, CreateView):
    page_title = "Add Video"


class LandingVideoUpdateView(LandingVideoFormView, UpdateView):
    page_title = "Update Video"


class LandingVideoDeleteView(LandingVideoView, DeleteView):
    page_title = "Delete Video"
    template_name = "administrator/base_confirm_delete.html"


class LandingAssetListView(AdministratorServiceMixin, ListView):
    page_title = "Landing Assets"
    template_name = "administrator/landing_asset_list.html"
    model = LandingCarousel
    context_object_name = "carousels"
    ordering = ['-is_active', 'ordering']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['popups'] = LandingPopup.objects.all()
        context['thin_banners'] = LandingThinBanner.objects.all()

        return context


class LandingCarouselFormView(AdministratorServiceMixin):
    model = LandingCarousel
    form_class = LandingCarouselForm
    template_name = "administrator/base_form.html"
    success_url = reverse_lazy('administrator:landing-asset-list')


class LandingCarouselCreateView(LandingCarouselFormView, CreateView):
    page_title = "Add Carousel"


class LandingCarouselUpdateView(LandingCarouselFormView, UpdateView):
    page_title = "Update Carousel"


class LandingCarouselDeleteView(AdministratorServiceMixin, DeleteView):
    page_title = "Delete Carousel"
    template_name = "administrator/base_confirm_delete.html"
    success_url = reverse_lazy('administrator:landing-asset-list')


class LandingPopupFormView(AdministratorServiceMixin):
    model = LandingPopup
    form_class = LandingPopupForm
    template_name = "administrator/base_form.html"
    success_url = reverse_lazy('administrator:landing-asset-list')


class LandingPopupCreateView(LandingPopupFormView, CreateView):
    page_title = "Add Popup"


class LandingPopupUpdateView(LandingPopupFormView, UpdateView):
    page_title = "Update Popup"


class LandingPopupDeleteView(AdministratorServiceMixin, DeleteView):
    page_title = "Delete Popup"
    template_name = "administrator/base_confirm_delete.html"
    success_url = reverse_lazy('administrator:landing-asset-list')


class LandingThinBannerFormView(AdministratorServiceMixin):
    model = LandingThinBanner
    form_class = LandingThinBannerForm
    template_name = "administrator/base_form.html"
    success_url = reverse_lazy('administrator:landing-asset-list')


class LandingThinBannerCreateView(LandingThinBannerFormView, CreateView):
    page_title = "Add Thin Banner"


class LandingThinBannerUpdateView(LandingThinBannerFormView, UpdateView):
    page_title = "Update Thin Banner"


class LandingThinBannerDeleteView(AdministratorServiceMixin, DeleteView):
    page_title = "Delete Thin Banner"
    template_name = "administrator/base_confirm_delete.html"
    success_url = reverse_lazy('administrator:landing-asset-list')


# FAQ Management
class FaqListView(AdministratorServiceMixin, ListView):
    model = Faq
    page_title = "FAQ"
    template_name = "administrator/faq_list.html"
    context_object_name = "faq_list"
    ordering = ['num']
    paginate_by = "20"


class FaqFormView(AdministratorServiceMixin):
    model = Faq
    success_url = reverse_lazy('administrator:faq-list')


class FaqCreateView(FaqFormView, CreateView):
    page_title = "Create FAQ"
    form_class = FaqForm
    template_name = 'administrator/faq_form.html'


class FaqUpdateView(FaqFormView, UpdateView):
    page_title = "Update FAQ"
    form_class = FaqForm
    template_name = 'administrator/faq_form.html'


class FaqDeleteView(FaqFormView, DeleteView):
    page_title = "Delete FAQ"
    template_name = 'administrator/faq_confirm_delete.html'
