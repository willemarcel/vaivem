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

from django.db import models
from django.contrib.auth.models import User
import datetime


class Usuario(models.Model):
    class Meta:
        ordering = ('nome',)

    CATEGORIAS_CAHL = (
        ('Estudante',(
            ('cinema', 'Cinema e Audiovisual'),
            ('comunicacao', 'Comunicação Social'),
            ('artes', 'Artes Visuais'),
            ('historia', 'História'),
            ('gestaopublica', 'Gestão Pública'),
            ('museologia', 'Museologia'),
            ('cienciassociais', 'Ciências Sociais'),
            ('servicosocial', 'Serviço Social'),
            )
        ),
        ('professor', 'Professor'),
        ('tecnico', 'Técnico Administrativo'),
	)
    nome = models.CharField(max_length=100)
    matricula = models.IntegerField(max_length=9, primary_key=True)
    categoria = models.CharField(max_length=50, choices=CATEGORIAS_CAHL)
    email = models.EmailField(max_length=75)
    telefone = models.CharField(max_length=15)
    endereco = models.TextField('Endereço', max_length=200)
    suspensao = models.DateField('Suspenso até', default=datetime.date(2010, 9, 7), null=True)
    disponivel = models.BooleanField(default=True)
    observacoes = models.TextField('Observações', max_length=300, blank=True)
    atualizacao_cadastral = models.DateField('Última atualização de cadastro', auto_now_add=True)
    def __unicode__(self):
        return self.nome


class Equipamento(models.Model):
    class Meta:
        ordering = ('nome','tombo',)

    CATEG_EQUIPOS = (
        ('audio', 'Áudio'),
        ('video', 'Vídeo'),
        ('foto', 'Fotografia'),
        ('info', 'Informática'),
        ('museu', 'Museologia')
    )
    tombo = models.IntegerField(max_length=10, primary_key=True)
    nome = models.CharField(max_length=200)
    numeroserie = models.CharField('Número de Série', max_length=30, null=True)
    categoria = models.CharField(max_length=50, choices=CATEG_EQUIPOS)
    disponivel = models.BooleanField(default=True)
    observacoes = models.TextField('Observações', max_length=300, blank=True)
    ultimo_inventario = models.DateField('Data do último inventário', null=True)
    def __unicode__(self):
        return u'%s - %s' % (self.tombo, self.nome)


class Emprestimo(models.Model):
    id = models.AutoField(primary_key=True)
    itens = models.ManyToManyField('Equipamento', limit_choices_to = {'disponivel':True})
    usuario = models.ForeignKey('Usuario', limit_choices_to = {'suspensao__lte':datetime.date.today(), 'atualizacao_cadastral__gte':datetime.date(2013,7,20)})
    data_emprestimo = models.DateTimeField('Data de Empréstimo', auto_now_add=True)
    prazo_devolucao = models.DateTimeField('Prazo para Devolução', null=True)
    data_devolucao = models.DateTimeField('Data de Devolução', null=True)
    devolvido = models.BooleanField(default=False)
    funcionario_emprestimo = models.ForeignKey(User, related_name="%(class)s_emprestimo", null=True)
    funcionario_devolucao = models.ForeignKey(User, related_name="%(class)s_devolucao", null=True)
    def __unicode__(self):
        return str(self.id)


