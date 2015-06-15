from dropbox.client import DropboxOAuth2Flow
from django.conf import settings
from django import http
from django.core.urlresolvers import reverse
from django.views.generic import View, RedirectView
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _

from poireau.common.views import BaseLoggedViewMixin
import logging

LOGGER = logging.getLogger(__name__)


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
            raise
            return http.HttpResponseForbidden()

        except DropboxOAuth2Flow.NotApprovedException as exc:
            messages.error(request, _("Application not authorized !"))
            return http.HttpResponseRedirect(reverse("home"))

        except DropboxOAuth2Flow.ProviderException as exc:
            LOGGER.error("Auth error: {}".format(exc))
            raise
            return http.HttpResponseForbidden()

        self.request.session["dropbox_access_token"] = access_token

        return http.HttpResponseRedirect(reverse("songs:song_discover"))


class DropboxTokenMixin(object):

    class NoToken(Exception):
        pass

    def dispatch(self, request, *args, **kwargs):
        try:
            self.dropbox_access_token = request.session["dropbox_access_token"]
        except KeyError:
            return http.HttpResponseRedirect(reverse("songs:dropbox_start"))
        return super(DropboxTokenMixin, self).dispatch(request, *args, **kwargs)
