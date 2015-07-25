#
#  Copyright (c) 2010 Wille Marcel Lima Malheiro and contributors
#
#  This file is part of VaiVem.
#
#  VaiVem is free software under terms of the GNU Affero General Public
#  License version 3 (AGPLv3) as published by the Free
#  Software Foundation. See the file README for copying conditions.
#


from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from emprestimo.views import page404

handler404 = page404
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^', include('emprestimo.urls', namespace='emprestimo')),
    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()
