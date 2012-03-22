# -*- coding: utf-8 -*-
#
#  Copyright (c) 2010 Wille Marcel Lima Malheiro and contributors
#
#  This file is part of VaiVem.
#
#  VaiVem is free software under terms of the GNU Affero General Public
#  License version 3 (AGPLv3) as published by the Free
#  Software Foundation. See the file README for copying conditions.
#

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
import datetime
from vaivem.emprestimo.models import Equipamento, Emprestimo, Usuario
from django.core.exceptions import ObjectDoesNotExist


def index(request):
    return HttpResponseRedirect('/vaivem/admin/')


# lista os empréstimos com link para o termo de empréstimo
def emprestimosindex(request):
    emps = Emprestimo.objects.filter(devolvido=False)
    return render_to_response('comprovante-emprestimo-index.html', {'emps': emps})


# gera os termos de responsabilidade dos empréstimos
def comprovanteemprestimo(request, emprestimo_id):
    obj = Emprestimo.objects.get(id=emprestimo_id)
    data_emp = obj.data_emprestimo.strftime("%d/%m/%Y - %H:%M")
    prazo_dev = obj.prazo_devolucao.strftime("%d/%m/%Y - %H:%M")
    return render_to_response('comprovante-emprestimo.html', {'obj': obj, 'data_emp': data_emp, 'prazo_dev': prazo_dev})


# generate the loans list
# gera os relatórios de emprestimo
def relatorio(request, emprestimo_id):
    obj = Emprestimo.objects.get(id=emprestimo_id)
    data_emp = obj.data_emprestimo.strftime("%d/%m/%Y - %H:%M")
    prazo_dev = obj.prazo_devolucao.strftime("%d/%m/%Y - %H:%M")
    if obj.devolvido == True:
        data_dev = obj.data_devolucao.strftime("%d/%m/%Y - %H:%M")
    else:
        data_dev = 'Ainda não foi devolvido'
    return render_to_response('relatorio.html', {'obj': obj, 'data_emp': data_emp, 'data_dev': data_dev, 'prazo_dev': prazo_dev})


# search forms of loans
# formulário de busca de empréstimos
def search_form(request):
    return render_to_response('search_form.html')


# search results
# resultados da busca
def search(request):
    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q']
        
        if request.GET['search_by'] == "equipamento":
            try:
                emps = Equipamento.objects.get(tombo=q).emprestimo_set.order_by('-id')
            except ObjectDoesNotExist:
                emps = []
        else:
            try:
                emps = Usuario.objects.get(matricula=q).emprestimo_set.order_by('-id')
            except ObjectDoesNotExist:
                emps = []

        if request.GET['devolvido'] == "true":
            emps = emps.filter(devolvido=True)
        elif request.GET['devolvido'] == "false":
            emps = emps.filter(devolvido=False)
            
        return render_to_response('search_results.html', {'emprestimos': emps, 'query': q})
    else:
        return render_to_response('search_form.html', {'error': True})

def page404(request):
    return render_to_response('404.html')


