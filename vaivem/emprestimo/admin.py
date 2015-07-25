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
import datetime

from django.contrib import admin, messages
from django.forms import Textarea
from django.db import models
from django.middleware import csrf
from django.shortcuts import render_to_response
from django import template
from django.http import HttpResponseRedirect
from django.contrib.admin import helpers
from django.contrib.auth.models import User, check_password

from .models import Usuario, Equipamento, Emprestimo


class UsuarioAdmin(admin.ModelAdmin):
    fields = ['matricula', 'nome', 'categoria', 'email', 'telefone','endereco', 'observacoes']
    list_display = ('nome', 'matricula', 'categoria', 'disponivel', 'suspensao', 'atualizacao_cadastral', 'observacoes')
    list_filter = ['categoria', 'disponivel', 'atualizacao_cadastral']
    search_fields = ('nome', 'matricula')
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':40})},
    }
    actions = ['listar_emprestimos', 'atualizar_cadastro', 'retirar_suspensao']

#action that lists loans of a user
#action que lista empréstimos de um usuario
    def listar_emprestimos(modeladmin, request, queryset):
        if len(queryset) > 1:
            messages.error(request, 'Erro! Selecione apenas um usuario de cada vez')
        else:
            return HttpResponseRedirect("/admin/procura/?q=%s&search_by=usuario&devolvido=not_matters" % queryset[0].matricula)

    listar_emprestimos.short_description = "Listar emprestimos"

# update 'atualizacao_cadastral' of a user to today
# action que altera data de atualizacao_cadastral para hoje
    def atualizar_cadastro(modeladmin, request, queryset):
        if len(queryset) > 1:
            messages.error(request, 'Erro! Selecione apenas um usuario de cada vez')
        else:
            for usuario in queryset:
                Usuario.objects.filter(matricula = usuario.matricula).update(atualizacao_cadastral = datetime.date.today())
                modeladmin.message_user(request, "Atualização cadastral realizada")

    atualizar_cadastro.short_description = "Realizar atualização cadastral"


# update 'atualizacao_cadastral' of the equipments to yesterday
# action que muda data de suspensão para o dia anterior
    def retirar_suspensao(modeladmin, request, queryset):
        if len(queryset) > 1:
            messages.error(request, 'Erro! Selecione apenas um usuario de cada vez')
        else:
            for usuario in queryset:
                Usuario.objects.filter(matricula = usuario.matricula).update(suspensao = datetime.date.today() - datetime.timedelta(1))
                modeladmin.message_user(request, "Suspensão retirada com sucesso")

    retirar_suspensao.short_description = "Retirar suspensão"


class EquipamentoAdmin(admin.ModelAdmin):
    fields = ['tombo', 'nome', 'numeroserie', 'categoria', 'observacoes']
    list_display = ('tombo', 'nome',  'numeroserie', 'categoria', 'disponivel', 'ultimo_inventario', 'observacoes')
    list_filter = ['categoria', 'disponivel', 'ultimo_inventario']
    search_fields = ('nome', 'tombo', 'numeroserie')
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs = {'rows':3, 'cols':40})},
    }
    actions = ['inventariar', 'listar_emprestimos', 'tornar_disponivel', 'nao_disponivel']

# list loans of a equipament
# lista emprestimos de um equipamento
    def listar_emprestimos(modeladmin, request, queryset):
        if len(queryset) > 1:
            messages.error(request, 'Erro! Selecione apenas um equipamento de cada vez')
        else:
            return HttpResponseRedirect("/admin/procura/?q=%s&search_by=equipamento&devolvido=not_matters" % queryset[0].tombo)

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
        if len(Emprestimo.objects.filter(itens__in = queryset).filter(devolvido = False)) > 0:
            if len(queryset) > 1:
                messages.error(request, 'Erro! Alguns dos equipamentos encontram-se emprestados')
            else:
                messages.error(request, 'Erro! O equipamento encontra-se emprestado')
        else:
            for equipo in queryset:
                Equipamento.objects.filter(tombo = equipo.tombo).update(disponivel=True)
                modeladmin.message_user(request, "Equipamento marcado como disponivel")

    tornar_disponivel.short_description = "Marcar como Disponivel"

# modify the verification date of the equipments to today
# action que altera data de inventário dos equipamentos para hoje
    def inventariar(modeladmin, request, queryset):
        for equipo in queryset:
            Equipamento.objects.filter(tombo = equipo.tombo).update(ultimo_inventario=datetime.date.today())
            modeladmin.message_user(request, "Data de inventário atualizada")

    inventariar.short_description = "Atualizar data de inventário"


class EmprestimoAdmin(admin.ModelAdmin):
    fields = ['usuario', 'itens', 'prazo_devolucao']
    filter_horizontal = ('itens',)
    list_display = ('id', 'usuario', 'prazo_devolucao', 'devolvido')
    list_filter = ['devolvido', 'data_emprestimo', 'prazo_devolucao', 'data_devolucao']
    actions = ['devolucao', 'comprovante_emprestimo']

# itens handover process
# processo de devolução de itens
    def devolucao(modeladmin, request, queryset):
        if len(queryset) > 1:
            messages.error(request, "Não é possível efetuar mais de uma devolução ao mesmo tempo")
        elif len(Emprestimo.objects.filter(id__in = queryset).filter(devolvido = 'True')) > 0:
            messages.error(request, "O empréstimo já foi devolvido")
        else:
            if 'post' in request.POST:
                Equipamento.objects.filter(emprestimo__in = queryset).update(disponivel = True)
                queryset.update(devolvido='True', data_devolucao = datetime.datetime.now(), funcionario_devolucao = request.user)


                # apply fees, if the handover is outdate
                # calcula e aplica multas, se a devolução for realizada com atraso
                for emp in queryset:
                    atraso = emp.data_devolucao - emp.prazo_devolucao
                    if atraso > datetime.timedelta(minutes=60):
                        if atraso < datetime.timedelta(hours=2):
                            multa = datetime.datetime.now() + datetime.timedelta(1)
                        elif atraso < datetime.timedelta(hours=3):
                            multa = datetime.datetime.now() + datetime.timedelta(2)
                        elif atraso < datetime.timedelta(hours=4):
                            multa = datetime.datetime.now() + datetime.timedelta(3)
                        elif atraso < datetime.timedelta(hours=24):
                            multa = datetime.datetime.now() + datetime.timedelta(5)
                        elif atraso < datetime.timedelta(hours=48):
                            multa = datetime.datetime.now() + datetime.timedelta(7)
                        elif atraso < datetime.timedelta(hours=72):
                            multa = datetime.datetime.now() + datetime.timedelta(15)
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

# mostrar comprovante de empréstimo
    def comprovante_emprestimo(modeladmin, request, queryset):
        if len(queryset) > 1:
            messages.error(request, 'Erro! Selecione apenas um empréstimo de cada vez')
        else:
            return HttpResponseRedirect("/admin/comprovante/emprestimo/%s" % queryset[0].id)

    comprovante_emprestimo.short_description = "Abrir comprovante de empréstimo"


    #saves loan and change status of users and equipaments
    # Salva os emprestimos e modifica o status do usuario e equipamentos
    def save_model(self, request, obj, form, change):
        obj.funcionario_emprestimo = request.user
        obj.save()
        m = form.save()
        m.usuario.disponivel = False
        m.usuario.save()
        for i in m.itens.all():
            i.disponivel = False
            i.save()


admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Equipamento, EquipamentoAdmin)
admin.site.register(Emprestimo, EmprestimoAdmin)
