from functools import wraps

from django.core.exceptions import PermissionDenied


def _ensure_admin_user(user):
    is_admin = user.is_staff and user.is_superuser
    if not is_admin:
        raise PermissionDenied


def require_admin_access(f):
    """Decorator to ensure the resource access is from an admin"""
    @wraps(f)
    def require_admin_access_decorator(*args, **kwargs):
        request = args[0].request
        _ensure_admin_user(request.user)
        return f(*args, **kwargs)

    return require_admin_access_decorator
