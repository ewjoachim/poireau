from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class BaseViewMixin(object):
    pass


class LoginRequiredMixin(object):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)


class BaseLoggedViewMixin(BaseViewMixin, LoginRequiredMixin):
    pass
