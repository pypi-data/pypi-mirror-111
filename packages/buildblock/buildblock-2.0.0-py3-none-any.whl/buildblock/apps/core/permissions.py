"""
Possible functions for the ``PRIVATE_STORAGE_AUTH_FUNCTION`` setting.
"""

def can_access_private_file(private_file):
    request = private_file.request
    return request.user.is_authenticated and (
        request.user.is_superuser
        or request.user.is_staff
        or str(request.user.uuid) in private_file.relative_name
    )
