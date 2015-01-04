from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.conf import settings
from django.views.generic import TemplateView, View


class BaseViewMixin(object):
    def get_context_data(self, **kwargs):
        context = super(BaseViewMixin, self).get_context_data(**kwargs)
        context["CHOIR_NAME"] = settings.CHOIR_NAME
        return context


class LoginRequiredMixin(object):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)


class BaseLoggedViewMixin(BaseViewMixin, LoginRequiredMixin):
    pass


class HomeView(BaseLoggedViewMixin, TemplateView):
    template_name = "base/home.html"

