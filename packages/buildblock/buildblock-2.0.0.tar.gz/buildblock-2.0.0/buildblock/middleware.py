from django.shortcuts import redirect
from django.urls import reverse


# https://docs.djangoproject.com/en/2.2/topics/http/middleware/#writing-your-own-middleware
class BaseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response


def is_request_of_first_visited_invited_user(request):
    return (
        request.user.is_authenticated and
        request.user.is_first_visited_invited_user and
        request.method == 'GET' and
        not request.path.startswith(reverse('welcome-invited-user'))
    )


class CustomMiddleware(BaseMiddleware):
    def __call__(self, request):
        # 초대 회원 첫 접속시 Redirect
        if is_request_of_first_visited_invited_user(request):
            return redirect(reverse('welcome-invited-user'))

        response = self.get_response(request)
        return response
