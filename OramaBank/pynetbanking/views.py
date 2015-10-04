# coding: utf-8

#--------------//////////----------------------

#Projeto Criado por: Lário Diniz
#Contatos: developer.lario@gmail.com
#data: 26/09/2015

#--------------//////////----------------------

from django.views.generic import View, DetailView, ListView, TemplateView
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, render_to_response
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.contrib import messages

import random
import datetime

from .forms import LoginForm, NewclintForm, AccountForm, OperacaoForm
from .models import Cliente_Model, Conta_Model

class ExitView(View):
    'View logout'
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect('/')

class loginView(TemplateView):
    'View Login'
    template_name = "pynetbanking/login.html"
    form_class = LoginForm
    initial = {'key': 'value'}

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            slug=Cliente_Model.objects.get(user=request.user).slug
            return HttpResponseRedirect('/clint/%s' %slug)
        else:
            form = self.form_class(initial=self.initial)
            return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.login(request)
            if user:
                login(request, user)
                slug=Cliente_Model.objects.get(user=request.user).slug
                return HttpResponseRedirect('/clint/%s' %slug)
        else:
            return render(request, self.template_name, {'form': form})

class NewuserViews(View):
    'View que cria novo cliente'
    template_name = 'pynetbanking/newclint.html'
    form_class = NewclintForm
    initial = {'key': 'value'}

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            slug=Cliente_Model.objects.get(user=request.user).slug
            return HttpResponseRedirect('/clint/%s' %slug)

        else:
            form = self.form_class(initial=self.initial)
            return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):

        form = self.form_class(request.POST)
        if form.is_valid():

            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            login(request, user)
            slug=Cliente_Model.objects.get(user=request.user.pk).slug
            return HttpResponseRedirect('/clint/%s' %slug)
        else:
            return render(request, self.template_name, {'form': form})

class ClintViews(DetailView):

    model = Cliente_Model
    template_name = 'pynetbanking/clint.html'

    def get_context_data(self, **kwargs):

        context = super(ClintViews, self).get_context_data(**kwargs)
        context['usuario'] = self.request.user.username
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ClintViews, self).dispatch(*args, **kwargs)

class NewaccountViews(View):
    template_name = 'pynetbanking/newaccount.html'
    form_class = AccountForm
    initial = {'key': 'value'}

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form, 'usuario':self.request.user.username})

    def post(self, request, *args, **kwargs):

        form = self.form_class(request.POST)
        if form.is_valid():

            n=str()
            for x in range(10):
                n+=str(random.randrange(0,9))

            Conta_Model.objects.create(
            user=self.request.user,
            data=timezone.now(),
            numero=n,
            saldo=form.cleaned_data['saldo'],
            tipo=form.cleaned_data['tipo'],).save()
            messages.success(request, "Conta Cadastrada com sucesso")
            slug=Cliente_Model.objects.get(user=self.request.user.pk).slug
            return HttpResponseRedirect('/clint/%s' %slug)
        else:
            return render(request, self.template_name, {'form': form, 'usuario':self.request.user.username})

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(NewaccountViews, self).dispatch(*args, **kwargs)

class AccountsViews(ListView):
    template_name = 'pynetbanking/acconts.html'
    model = Conta_Model

    def get_context_data(self, **kwargs):

        context = super(AccountsViews, self).get_context_data(**kwargs)
        context['object_list']= Conta_Model.objects.filter(user=self.request.user)
        context['usuario'] = self.request.user.username
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AccountsViews, self).dispatch(*args, **kwargs)
"""
Função para o próprio usuario deletar saus contas, Comentada pois esta funcionalidade não foi exigida.

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        self.request.session['conta']= request.POST['button']
        return render(request, self.template_name, {'form': form, 'usuario':self.request.user.username})

class DelAccountViews(TemplateView):
    template_name = "pynetbanking/delaccont.html"

    def get_context_data(self, **kwargs):
        context = super(DelAccountViews, self).get_context_data(**kwargs)
        context['usuario'] = self.request.user.username
        context['conta'] = Conta_Model.objects.get(pk=int(self.request.COOKIES['conta']))
        return context

    def post(self, request, *args, **kwargs):
        Conta_Model.objects.get(pk=int(self.request.session['conta'])).delete()
        self.request.session['conta']=''
        #FALTA RETURN
"""
class AccountViews(DetailView):
    model = Conta_Model
    template_name = 'pynetbanking/accont.html'


    def get_context_data(self, **kwargs):
        context = super(AccountViews, self).get_context_data(**kwargs)
        context['usuario'] = self.request.user.username
        self.request.session['conta']=context['object'].pk
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AccountViews, self).dispatch(*args, **kwargs)


class DepositoViews(View):
    template_name = 'pynetbanking/Operacao.html'
    form_class = OperacaoForm
    initial = {'key': 'value'}

    def get(self, request, *args, **kwargs):
        c=Conta_Model.objects.get(pk=int(self.request.session['conta']))
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name,
                      {'form': form,
                       'usuario':self.request.user.username,
                       'operacao':'Deposito',
                       'conta':c.numero,
                       })


    def post(self, request, *args, **kwargs):

        form = self.form_class(request.POST)
        if form.is_valid():

            c=Conta_Model.objects.get(pk=int(self.request.session['conta']))
            c.operacao('deposito', float(form.cleaned_data['valor']))
            messages.success(request, "Deposito de %s feito na conta %s com sucesso" %(form.cleaned_data['valor'], c))
            self.request.session['conta']=''
            return HttpResponseRedirect('/accounts/')
        else:
            return render(request, self.template_name, {'form': form, 'usuario':self.request.user.username})


    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(DepositoViews, self).dispatch(*args, **kwargs)

class SaqueViews(View):
    template_name = 'pynetbanking/operacao.html'
    form_class = OperacaoForm
    initial = {'key': 'value'}

    def get(self, request, *args, **kwargs):
        c=Conta_Model.objects.get(pk=int(self.request.session['conta']))
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name,
                      {'form': form,
                       'usuario':self.request.user.username,
                       'operacao':'Saque',
                       'conta':c.numero,
                       })


    def post(self, request, *args, **kwargs):

        form = self.form_class(request.POST)
        if form.is_valid():

            c=Conta_Model.objects.get(pk=int(self.request.session['conta']))
            c.operacao('saque', float(form.cleaned_data['valor']))
            messages.success(request, "Saque de %s feito na conta %s com sucesso" %(form.cleaned_data['valor'], c))
            self.request.session['conta']=''
            return HttpResponseRedirect('/accounts/')
        else:
            return render(request, self.template_name, {'form': form, 'usuario':self.request.user.username})


    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(SaqueViews, self).dispatch(*args, **kwargs)