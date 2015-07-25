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
from vaivem.emprestimo.views import emprestimosindex, comprovanteemprestimo, relatorio, search_form, search, stats



urlpatterns = patterns('',
    # Example:
    (r'^$', 'vaivem.emprestimo.views.index'),
    (r'^admin/comprovante/emprestimo/(?P<emprestimo_id>\d+)/$', comprovanteemprestimo),
    (r'^admin/comprovante/emprestimo/$', emprestimosindex),
    (r'^admin/emprestimo/emprestimo/(?P<emprestimo_id>\d+)/$', relatorio),
    (r'^admin/buscador/$', search_form),
    (r'^admin/procura/$', search),
    (r'^admin/stats/$', stats),
)
