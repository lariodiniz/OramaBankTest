# coding: utf-8

#--------------//////////----------------------

#Projeto Criado por: Lário Diniz
#Contatos: developer.lario@gmail.com
#data: 30/09/2015

#--------------//////////----------------------

from django.contrib import admin
from django.utils.translation import ugettext as _
from datetime import datetime
from django.utils import timezone

from .models import Cliente_Model, Conta_Model, Operacao_model

class Cliente_ModelnAdmin(admin.ModelAdmin):
    list_display = ('user', 'codigo', 'cpf', 'saldo_total','conta_corrente','poupanca')
    search_fields = ['user', 'codigo', 'cpf']

    def saldo_total(self, obj):
        contas =  Conta_Model.objects.filter(user=Cliente_Model.objects.get(user=obj.user))
        saldo = float()


        for conta in contas:
            saldo += conta.saldo

        return saldo

    def conta_corrente(self, obj):
        contas =  Conta_Model.objects.filter(user=Cliente_Model.objects.get(user=obj.user))
        val=False

        for conta in contas:
            if conta.tipo=='0':
                val=True

        return val

    saldo_total.short_description=_('Saldo Total')
    conta_corrente.short_description=_('Possui Conta Corrente?')
    conta_corrente.boolean = True

    def poupanca(self, obj):
        contas =  Conta_Model.objects.filter(user=Cliente_Model.objects.get(user=obj.user))
        val=False

        for conta in contas:
            if conta.tipo=='1':
                val=True

        return val

    saldo_total.short_description=_('Saldo Total')
    conta_corrente.short_description=_('Possui Conta Corrente?')
    conta_corrente.boolean = True
    poupanca.short_description=_('Possui Poupanca?')
    poupanca.boolean = True


class Conta_ModelAdmin(admin.ModelAdmin):
    list_display = ('numero','user','tipo', 'saldo', 'data')
    list_filter = ['data']
    search_fields = ['numero']



class Operacao_ModelAdmin(admin.ModelAdmin):
    list_display = ('conta','tipo','valor','data')
    list_filter = ['data', 'tipo']


admin.site.register(Cliente_Model, Cliente_ModelnAdmin)
admin.site.register(Conta_Model, Conta_ModelAdmin)
admin.site.register(Operacao_model, Operacao_ModelAdmin)




