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

from vaivem.emprestimo.models import Usuario
from vaivem.emprestimo.models import Equipamento
from vaivem.emprestimo.models import Emprestimo
from django.contrib import admin
import datetime
from django.forms import Textarea
from django.db import models
from django.middleware import csrf
from django.shortcuts import render_to_response
from django import template
from django.http import HttpResponseRedirect
from django.contrib.admin import helpers
from django.contrib import messages
from django.contrib.auth.models import User, check_password


class UsuarioAdmin(admin.ModelAdmin):
    fields = ['matricula', 'nome', 'categoria', 'email', 'telefone','endereco', 'observacoes']
    list_display = ('nome', 'matricula', 'categoria', 'disponivel', 'suspensao', 'observacoes')
    list_filter = ['categoria', 'disponivel']
    search_fields = ('nome', 'matricula')
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':40})},
    }
    actions = ['listar_emprestimos']

    def listar_emprestimos(modeladmin, request, queryset):
        if len(queryset) > 1:
            messages.error(request, 'Erro! Selecione apenas um usuario de cada vez')
        else:
            return HttpResponseRedirect("/vaivem/admin/procura/?q=%s&search_by=usuario&devolvido=not_matters" % queryset[0].matricula)

    listar_emprestimos.short_description = "Listar emprestimos"


class EquipamentoAdmin(admin.ModelAdmin):
    fields = ['tombo', 'nome', 'numeroserie', 'categoria', 'observacoes']
    list_display = ('tombo', 'nome',  'numeroserie', 'categoria', 'disponivel', 'observacoes')
    list_filter = ['categoria', 'disponivel']
    search_fields = ('nome', 'tombo', 'numeroserie')
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs = {'rows':3, 'cols':40})},
    }
    actions = ['nao_disponivel', 'tornar_disponivel', 'listar_emprestimos']

    def listar_emprestimos(modeladmin, request, queryset):
        if len(queryset) > 1:
            messages.error(request, 'Erro! Selecione apenas um equipamento de cada vez')
        else:
            return HttpResponseRedirect("/vaivem/admin/procura/?q=%s&search_by=equipamento&devolvido=not_matters" % queryset[0].tombo)

    listar_emprestimos.short_description = "Listar emprestimos"

# modify the status of the equipment to disponible = True 
# action que altera status do equipamento para disponivel = False
    def nao_disponivel(modeladmin, request, queryset):
        for equipo in queryset:
            Equipamento.objects.filter(tombo = equipo.tombo).update(disponivel = False)
            modeladmin.message_user(request, "Equipamento marcado como Indisponivel")

    nao_disponivel.short_description = "Marcar como Indisponivel"

# modify the status of the equipment to disponible only if it's not loan 
# action que altera status do equipamento para disponivel = True, caso ele nao esteja emprestado
    def tornar_disponivel(modeladmin, request, queryset):
        if len(Emprestimo.objects.filter(item__in = queryset).filter(devolvido = False)) > 0:
            if len(queryset) > 1:
                messages.error(request, 'Erro! Alguns dos equipamentos encontram-se emprestados')
            else:
                messages.error(request, 'Erro! O equipamento encontra-se emprestado')
        else:
            for equipo in queryset:
                Equipamento.objects.filter(tombo = equipo.tombo).update(disponivel=True)
                modeladmin.message_user(request, "Equipamento marcado como disponivel")

    tornar_disponivel.short_description = "Marcar como Disponivel"


class EmprestimoAdmin(admin.ModelAdmin):
    fields = ['usuario', 'item', 'prazo_devolucao']
    filter_horizontal = ('item',)
    list_display = ('id', 'usuario', 'prazo_devolucao', 'devolvido')
    list_filter = ['devolvido', 'data_emprestimo', 'prazo_devolucao', 'data_devolucao']
    actions = ['devolucao']


# itens handover process
# processo de devolução de itens
    def devolucao(modeladmin, request, queryset):
        if len(queryset) > 1:
            modeladmin.message_user(request, "Não é possível efetuar mais de uma devolução ao mesmo tempo")
        elif len(Emprestimo.objects.filter(id__in = queryset).filter(devolvido = 'True')) > 0:
            modeladmin.message_user(request, "O empréstimo já foi devolvido")
        else:
            if 'post' in request.POST:
                Equipamento.objects.filter(emprestimo__in = queryset).update(disponivel = True)
                queryset.update(devolvido='True', data_devolucao = datetime.datetime.now(), funcionario_devolucao = request.user)


                # apply fees, if the handover is outdate 
                # calcula e aplica multas, se a devolução for realizada com atraso
                for emp in queryset:
                    atraso = emp.data_devolucao - emp.prazo_devolucao
                    if atraso > datetime.timedelta(minutes=15):
                        if atraso < datetime.timedelta(hours=8):
                            multa = datetime.datetime.now() + datetime.timedelta(2)
                        elif atraso < datetime.timedelta(hours=12):
                            multa = datetime.datetime.now() + datetime.timedelta(4)
                        elif atraso < datetime.timedelta(hours=24):
                            multa = datetime.datetime.now() + datetime.timedelta(10)
                        else:
                            multa = datetime.datetime.now() + datetime.timedelta(30)
                        Usuario.objects.filter(emprestimo = emp).update(suspensao = multa.date() , disponivel=True)
                    else:
                        Usuario.objects.filter(emprestimo = emp).update(disponivel = True)

                modeladmin.message_user(request, "Empréstimo devolvido com sucesso!")
                # Return to the list page
                return HttpResponseRedirect(request.get_full_path())

            # Render the confirmation page
            return render_to_response('devolucao.html', {'itens': Equipamento.objects.filter(emprestimo__in = queryset), 'queryset': queryset, 'action_checkbox_name': helpers.ACTION_CHECKBOX_NAME, 'csrf_token': csrf.get_token(request)})

    devolucao.short_description = "Marcar emprestimo como devolvido"


    #saves emprestimos and change status of usuario and equipamentos
    # Salva os emprestimos e modifica o status do usuario e equipamentos
    def save_model(self, request, obj, form, change):
        obj.funcionario_emprestimo = request.user
        obj.save()
        m = form.save()
        m.usuario.disponivel = False
        m.usuario.save()
        for i in m.item.all():
            i.disponivel = False
            i.save()


admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Equipamento, EquipamentoAdmin)
admin.site.register(Emprestimo, EmprestimoAdmin)
