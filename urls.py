#
#  Copyright (c) 2010 Wille Marcel Lima Malheiro and contributors
#
#  This file is part of VaiVem.
#
#  VaiVem is free software under terms of the GNU Affero General Public
#  License version 3 (AGPLv3) as published by the Free
#  Software Foundation. See the file README for copying conditions.
#


from django.conf.urls.defaults import *
from vaivem.emprestimo.views import emprestimosindex, comprovanteemprestimo, relatorio, search_form, search, page404

handler404 = page404
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    (r'^vaivem/$', 'vaivem.emprestimo.views.index'),
    (r'^vaivem/admin/comprovante/emprestimo/(?P<emprestimo_id>\d+)/$', comprovanteemprestimo),
    (r'^vaivem/admin/comprovante/emprestimo/$', emprestimosindex),
    (r'^vaivem/admin/emprestimo/emprestimo/(?P<emprestimo_id>\d+)/$', relatorio),
    (r'^vaivem/admin/buscador/$', search_form),
    (r'^vaivem/admin/procura/$', search),
# Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^vaivem/admin/', include(admin.site.urls)),
)
