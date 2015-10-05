# coding: utf-8

#--------------//////////----------------------

#Projeto Criado por: Lário Diniz
#Contatos: developer.lario@gmail.com
#data: 26/09/2015

#--------------//////////----------------------

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from django.utils import timezone
from django.db.models import signals


import datetime


class Cliente_Model(models.Model):
    """
    Modelo dos Clientes.
    """
    user=models.OneToOneField(User,verbose_name=_('Cliente'), blank=True)
    codigo=models.CharField(_(u'Códico'), max_length=250)
    cpf=models.CharField(_(u'CPF'))
    slug = models.SlugField(_('slug'),max_length=100, blank=True, unique=True)

    class Meta:
        verbose_name = _(u'Cliente')
        verbose_name_plural = _(u'Clientes')

    def get_absolute_url(self):

        return reverse('clint', kwargs={'slug': self.slug})

    def __str__(self):
        return self.user.username


class Conta_Model(models.Model):
    """
    Modelo das contas dos clientes.
    """
    user=models.ForeignKey(Cliente_Model,verbose_name=_('Cliente'), blank=True)
    numero=models.CharField(_(u'Conta'), max_length=250, blank=True, unique=True)
    data=models.DateTimeField(_('Conta Aberta'))
    saldo=models.FloatField(_('Saldo'))
    Tipos=(('0', 'conta corrente'), ('1', 'poupança'))
    tipo=models.CharField(_(u'Tipo'),choices=Tipos, default=0, max_length=1)

    def __str__(self):
        return 'Numero: '+str(self.numero)

    def operacao(self, tipo, valor):
        """
        Recebe um tipo de operacao e um valor ponto flutuante, faz a operação no saldo da conta.
        parametros: e salva um histórico da operaçao no modelo Operacao_model.
        Tipo: Os Tipo de transação pode ser "saque" ou "deposito".
        Valor: Valor que esta sendo movido do saldo da conta.

        """

        if tipo == "saque":
            self.saldo-=valor
            self.save()
            Operacao_model.objects.create(
                conta=self,
                tipo=tipo,
                data=timezone.now(),
                valor=valor
            ).save()
        elif tipo == "deposito":
            print "Estamos aqui"
            self.saldo+=valor
            self.save()
            Operacao_model.objects.create(
                conta=self,
                tipo=tipo,
                data=timezone.now(),
                valor=valor
            ).save()
        else:
            print "Tipo de operação não definido"

    class Meta:
        verbose_name = _(u'Conta')
        verbose_name_plural = _(u'Contas')

    def get_absolute_url(self):
        return reverse('account', kwargs={'pk': self.pk})

class Operacao_model(models.Model):
    """
    Modelo que armazena as operações executadas.
    """
    conta=models.ForeignKey(Conta_Model,verbose_name=_('Cliente'), blank=True)
    tipo=models.CharField(_(u'Tipo'), max_length=250)
    data=models.DateTimeField(_('Conta Aberta'))
    valor=models.FloatField(_('valor'))

    class Meta:
        ordering = ['-data']
        verbose_name = _(u'Histórico de operações')
        verbose_name_plural = _(u'Históricos de operações')


def create_clint(signal, instance, sender, **kwargs):
    """Este signal gera um slug automaticamente. Ele verifica se ja existe um
    cliente com o mesmo slug e acrescenta um numero ao final para evitar
    duplicidade"""
    if not instance.slug:
        slug = slugify(instance.user.username)
        novo_slug = slug
        contador = 0

        while Cliente_Model.objects.filter(slug=novo_slug).exclude(id=instance.id).count() > 0:
            contador += 1
            novo_slug = '%s-%d'%(slug, contador)

        instance.slug = novo_slug

signals.pre_save.connect(create_clint, sender=Cliente_Model)