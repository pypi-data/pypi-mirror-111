from modeltranslation.translator import TranslationOptions, register

from buildblock.apps.landing.models import History, Team, LandingVideo, LandingCarousel, LandingThinBanner, LandingPopup


@register(History)
class HistoryTranslationOptions(TranslationOptions):
    fields = ('title', 'subtitle')


@register(Team)
class TeamTranslationOptions(TranslationOptions):
    fields = ('name', 'work_experience', 'education', 'description')


@register(LandingVideo)
class LandingVideoTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


@register(LandingCarousel)
class LandingCarouselTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'button_title', 'image', 'image_mobile')


@register(LandingThinBanner)
class LandingThinBannerTranslationOptions(TranslationOptions):
    fields = ('title', 'image', 'image_mobile')


@register(LandingPopup)
class LandingPopupTranslationOptions(TranslationOptions):
    fields = ('title', 'image', 'image_mobile')
