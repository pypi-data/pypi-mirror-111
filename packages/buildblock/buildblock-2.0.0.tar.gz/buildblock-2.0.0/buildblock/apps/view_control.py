from django.contrib import messages

from buildblock.apps.core.constants import MSG_WRONG_APPROACH


def is_valid_post_request(request):
    if request.method != 'POST':
        messages.warning(request, MSG_WRONG_APPROACH)
        return False
    return True
