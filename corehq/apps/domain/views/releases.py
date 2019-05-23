from __future__ import absolute_import
from __future__ import unicode_literals

import json
from datetime import datetime
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy
from django.utils.functional import cached_property
from django.shortcuts import redirect
from django.http.response import HttpResponse, HttpResponseForbidden
from django.views.decorators.http import require_POST
from django.core.exceptions import ValidationError
from django.contrib import messages

from corehq import toggles
from corehq.apps.app_manager.dbaccessors import get_brief_apps_in_domain
from corehq.apps.app_manager.models import AppReleaseByLocation
from corehq.apps.domain.forms import ManageAppReleasesForm
from corehq.apps.domain.views import BaseProjectSettingsView
from corehq.apps.domain.decorators import login_and_domain_required
from corehq.apps.locations.models import SQLLocation


@method_decorator([toggles.MANAGE_RELEASES_PER_LOCATION.required_decorator()], name='dispatch')
class ManageReleases(BaseProjectSettingsView):
    template_name = 'domain/manage_releases.html'
    urlname = 'manage_releases'
    page_title = ugettext_lazy("Manage Releases")

    @cached_property
    def manage_releases_form(self):
        form = ManageAppReleasesForm(
            self.request,
            self.domain,
            data=self.request.POST if self.request.method == "POST" else None,
        )
        return form

    @staticmethod
    def _location_path_display(location_id):
        return SQLLocation.active_objects.get(location_id=location_id).get_path_display()

    @property
    def page_context(self):
        app_names = {app.id: app.name for app in get_brief_apps_in_domain(self.domain, include_remote=True)}
        q = AppReleaseByLocation.objects.filter(domain=self.domain)
        location_id_slug = self.request.GET.get('location_id')
        location_id = None
        if location_id_slug:
            location_id = self.manage_releases_form.extract_location_id(location_id_slug)
            if location_id:
                q = q.filter(location_id=location_id)
        if self.request.GET.get('app_id'):
            q = q.filter(app_id=self.request.GET.get('app_id'))
        version = self.request.GET.get('version')
        if version:
            q = q.filter(version=version)

        app_releases_by_location = [release.to_json() for release in q]
        for r in app_releases_by_location:
            r['app'] = app_names.get(r['app'], r['app'])
        return {
            'manage_releases_form': self.manage_releases_form,
            'app_releases_by_location': app_releases_by_location,
            'selected_build_details': ({'id': version, 'text': version} if version else None),
            'selected_location_details': ({'id': location_id_slug,
                                           'text': self._location_path_display(location_id)}
                                          if location_id else None),
        }

    def post(self, request, *args, **kwargs):
        if self.manage_releases_form.is_valid():
            success, error_message = self.manage_releases_form.save()
            if success:
                return redirect(self.urlname, self.domain)
            else:
                messages.error(request, error_message)
                return self.get(request, *args, **kwargs)
        else:
            return self.get(request, *args, **kwargs)


@login_and_domain_required
@require_POST
def deactivate_release_restriction(request, domain, restriction_id):
    return update_release_restriction(request, domain, restriction_id, active=False)


@login_and_domain_required
@require_POST
def activate_release_restriction(request, domain, restriction_id):
    return update_release_restriction(request, domain, restriction_id, active=True)


def update_release_restriction(request, domain, restriction_id, active):
    if not toggles.MANAGE_RELEASES_PER_LOCATION.enabled_for_request(request):
        return HttpResponseForbidden()
    release = AppReleaseByLocation.objects.get(id=restriction_id, domain=domain)
    try:
        release.activate() if active else release.deactivate()
    except ValidationError as e:
        response_content = {
            'message': ','.join(e.messages)
        }
    else:
        response_content = {
            'id': restriction_id,
            'success': True,
            'activated_on': (datetime.strftime(release.activated_on, '%Y-%m-%d %H:%M:%S')
                             if release.activated_on else None),
            'deactivated_on': (datetime.strftime(release.deactivated_on, '%Y-%m-%d %H:%M:%S')
                               if release.deactivated_on else None),
        }
    return HttpResponse(json.dumps(response_content), content_type='application/json')
