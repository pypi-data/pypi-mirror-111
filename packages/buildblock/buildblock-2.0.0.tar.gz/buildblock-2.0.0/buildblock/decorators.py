import logging
from functools import wraps

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import NoReverseMatch, reverse
from django.utils.translation import ugettext_lazy as _

from buildblock.apps.core.constants import MSG_WRONG_APPROACH
from buildblock.errors import RequiredPostDataError

_kwd_mark = object()  # sentinel for separating args from kwargs
logger = logging.getLogger(__name__)


def _get_key(args, kwargs):
    return args + (_kwd_mark,) + tuple(sorted(kwargs.items()))


class memoized_property(object):
    """
    A decorator that executes a method once and caches the result.  This can
    be used in place of @property if the calculations performed by the property
    only need to be executed once.
    """
    def __init__(self, func):
        self.__doc__ = func.__doc__
        self.func = func
        self.name = "_memoized_property__" + func.__name__

    def __get__(self, instance, cls):
        if instance is None:
            return self
        if hasattr(instance, self.name):
            return getattr(instance, self.name)
        result = self.func(instance)
        setattr(instance, self.name, result)
        return result


def memoize(fcn):
    """
    Decorator to memoize the return value of a function or method.
    """
    memoized_value = {}

    @wraps(fcn)
    def wrapped(*args, **kwargs):
        key = _get_key(args, kwargs)

        try:
            return memoized_value[key]

        except TypeError:
            # A TypeError will occur if the key contains unhashable types,
            # like lists or dicts.
            return fcn(*args, **kwargs)

        except KeyError:
            # A KeyError will occur if the value has not been cached yet,
            # but the key is cacheable.
            memoized_value[key] = fcn(*args, **kwargs)
            return memoized_value[key]

    def reset_memo(*args, **kwargs):
        memoized_value.clear()

    wrapped.reset_memo = reset_memo
    return wrapped


class classproperty(property):
    """Decorator to create a property on a class object"""
    def __get__(self, cls, owner):
        return classmethod(self.fget).__get__(None, owner)()


def memoized_classproperty(f):
    return classproperty(memoize(f))


def require_post(app):
    def decorator(func):
        @wraps(func)
        def inner(request, *args, **kwargs):
            if request.method != "POST":
                messages.warning(request, MSG_WRONG_APPROACH)
                try:
                    return HttpResponseRedirect(reverse(app+':home'))
                except NoReverseMatch:
                    return HttpResponseRedirect(reverse('home'))
            return func(request, *args, **kwargs)
        return inner
    return decorator


def catch_errors(func):
    @wraps(func)
    def inner(request, *args, **kwargs):
        try:
            return func(request, *args, **kwargs)
        except RequiredPostDataError:
            messages.error(request, _('Please enter the required information.'))
        except Exception as e:
            logger.error(f'Error has occurred while {func.__name__}: {str(e)}')
            messages.warning(request, _("Request Failed. Please try again."))
        finally:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return inner
