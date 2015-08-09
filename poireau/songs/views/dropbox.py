import logging

from dropbox.client import DropboxOAuth2Flow

from django.conf import settings
from django import http
from django.core.urlresolvers import reverse
from django.views.generic import View, RedirectView
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _

from poireau.common.views import BaseLoggedViewMixin

LOGGER = logging.getLogger(__name__)

DROPBOX_TOKEN_SESSION_KEY = "dropbox_access_token"


class DropboxMixin(object):
    def get_dropbox_auth_flow(self):
        redirect_uri = self.request.build_absolute_uri(reverse("songs:dropbox_finish"))
        return DropboxOAuth2Flow(settings.DROPBOX_APP_KEY, settings.DROPBOX_APP_SECRET, redirect_uri,
                                 self.request.session, "dropbox-auth-csrf-token")


class DropboxStartView(BaseLoggedViewMixin, DropboxMixin, RedirectView):
    permanent = True

    def get_redirect_url(self):
        authorize_url = self.get_dropbox_auth_flow().start()
        return authorize_url


class DropboxFinishView(BaseLoggedViewMixin, DropboxMixin, View):
    # URL handler for /dropbox-auth-finish
    def get(self, request):
        try:
            access_token, __, __ = self.get_dropbox_auth_flow().finish(self.request.GET)

        except DropboxOAuth2Flow.BadRequestException as exc:
            return http.HttpResponseBadRequest()

        except DropboxOAuth2Flow.BadStateException as exc:
            # Start the auth flow again.
            return http.HttpResponseRedirect(reverse("songs:dropbox_start"))

        except DropboxOAuth2Flow.CsrfException as exc:
            LOGGER.error("CSRF error: {}".format(exc))
            return http.HttpResponseForbidden()

        except DropboxOAuth2Flow.NotApprovedException as exc:
            messages.error(request, _("You have not authorized the application."))
            return http.HttpResponseRedirect(reverse("home"))

        except DropboxOAuth2Flow.ProviderException as exc:
            LOGGER.error("Auth error: {}".format(exc))
            return http.HttpResponseForbidden()

        request.session[DROPBOX_TOKEN_SESSION_KEY] = access_token
        request.user.dropbox_token = access_token
        request.user.save()

        return http.HttpResponseRedirect(reverse("songs:songs_choose_folder_dropbox"))


class DropboxTokenMixin(object):

    class NoToken(Exception):
        pass

    def dispatch(self, request, *args, **kwargs):
        self.dropbox_access_token = ""
        try:
            self.dropbox_access_token = request.session[DROPBOX_TOKEN_SESSION_KEY]
        except KeyError:
            pass

        if not self.dropbox_access_token:
            self.dropbox_access_token = request.session[DROPBOX_TOKEN_SESSION_KEY] = request.user.dropbox_token

        if self.dropbox_access_token:
            return super(DropboxTokenMixin, self).dispatch(request, *args, **kwargs)
        else:
            return http.HttpResponseRedirect(reverse("songs:dropbox_start"))
