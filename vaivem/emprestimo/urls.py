#
#  Copyright (c) 2010 Wille Marcel Lima Malheiro and contributors
#
#  This file is part of VaiVem.
#
#  VaiVem is free software under terms of the GNU Affero General Public
#  License version 3 (AGPLv3) as published by the Free
#  Software Foundation. See the file README for copying conditions.
#

from django.conf.urls import patterns, url

from .views import index, emprestimosindex, comprovanteemprestimo, relatorio, search_form, search, stats


urlpatterns = patterns('',
    # Example:
    url(r'^$', index, name='index'),
    url(r'^admin/comprovante/emprestimo/(?P<emprestimo_id>\d+)/$',
        comprovanteemprestimo,
        name='comprovanteemprestimo'),
    url(r'^comprovantes/$', emprestimosindex, name='comprovantes'),
    url(r'^admin/emprestimo/emprestimo/(?P<emprestimo_id>\d+)/$',
        relatorio,
        name='relatorio'),
    url(r'^admin/buscador/$', search_form, name='buscador'),
    url(r'^admin/procura/$', search, name='procura'),
    url(r'^admin/stats/$', stats, name='stats'),
)
