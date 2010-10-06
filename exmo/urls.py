# This file is part of EXMO2010 software.
# Copyright 2010 Al Nikolov
# Copyright 2010 Institute for Information Freedom Development
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings
from django.http import HttpResponsePermanentRedirect
from django.core.urlresolvers import reverse
admin.autodiscover()

urlpatterns = patterns('',
  #(r'^admin/(.*)', admin.site.root),
  (r'^admin/', include(admin.site.urls)),
  (r'^comments/', include('django.contrib.comments.urls')),
  (r'^exmo2010/', include('exmo.exmo2010.urls')),
  (r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'exmo2010/login.html'}),
  (r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'template_name': 'exmo2010/logged_out.html'}),
  (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT} ),
  (r'^accounts/password_change$', 'django.contrib.auth.views.password_change', {'template_name':'exmo2010/password_change_form.html' }),
  (r'^accounts/password_change/done$', 'django.contrib.auth.views.password_change_done', {'template_name':'exmo2010/password_change_done.html' }),
  (r'^accounts/profile/(\d+)$','exmo.exmo2010.views.user_profile'),
  (r'^$',lambda request: HttpResponsePermanentRedirect(reverse('exmo.exmo2010.views.monitoring_list'))),
)
