from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.conf import settings
from django.views.generic import TemplateView, View
from django.contrib.auth import views as django_auth_views


class BaseViewMixin(object):
    def get_context_data(self, **kwargs):
        context = super(BaseViewMixin, self).get_context_data(**kwargs)
        context["CHOIR_NAME"] = settings.CHOIR_NAME
        context["menu_list"] = getattr(self, "menu_list", [])
        return context


class LoginRequiredMixin(object):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)


class BaseLoggedViewMixin(BaseViewMixin, LoginRequiredMixin):
    pass


class HomeView(BaseLoggedViewMixin, TemplateView):
    template_name = "base/home.html"
    menu_list = ["home"]


class LoginView(BaseViewMixin, TemplateView):
    template_name = "auth/login.html"

    def dispatch(self, request, *args, **kwargs):
        return django_auth_views.login(
            request=request, template_name=self.template_name,
            extra_context=self.get_context_data()
        )


class LogoutView(BaseViewMixin, View):
    template_name = "auth/logout.html"

    def dispatch(self, request, *args, **kwargs):
        return django_auth_views.logout_then_login(
            request=request
        )
