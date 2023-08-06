import logging

from django.conf import settings
from django.contrib.auth import login
from django.urls import reverse

from buildblock.apps.core.views import RedirectView
from buildblock.apps.signed_url.handler import EXPIRATION_DATE_TIMESTAMP, URL_TO_REDIRECT, USER_EMAIL, SignedUrlHandler
from buildblock.apps.users.models import User

logger = logging.getLogger(__name__)


class SignedUrlRedirectView(RedirectView):

    permanent = False
    query_string = True

    def get_redirect_url(self, *args, **kwargs):
        query_parameters = self.request.GET

        # 1. Check parameter
        if not SignedUrlHandler.has_required_parameters(query_parameters):
            logger.warning(f'Missing required params : {query_parameters}')
            return reverse('signed-url-invalid')

        # 2. Check Expiration
        if SignedUrlHandler.is_expired(query_parameters[EXPIRATION_DATE_TIMESTAMP]):
            logger.warning(f'is_expired : {query_parameters[EXPIRATION_DATE_TIMESTAMP]}')
            return reverse('signed-url-expired')

        # 3. Validate Signature
        if SignedUrlHandler.is_valid_signature(query_parameters):
            try:
                user = User.objects.get(email=query_parameters[USER_EMAIL])
            except User.DoesNotExist:
                logger.warning(f'User does not exist : {query_parameters[USER_EMAIL]}')
                return reverse('signed-url-invalid')
            except Exception as e:
                logger.error(f'{e} : {query_parameters[USER_EMAIL]}', exc_info=True)
                raise
            user.backend = settings.DJANGO_AUTH_MODEL_BACKEND
            login(self.request, user)

            return query_parameters[URL_TO_REDIRECT]

        logger.info(f'Invalid request : {query_parameters}')
        return reverse('signed-url-invalid')
