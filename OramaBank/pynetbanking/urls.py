# coding: utf-8

#--------------//////////----------------------

#Projeto Criado por: Lário Diniz
#Contatos: developer.lario@gmail.com
#data: 26/09/2015

#--------------//////////----------------------

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^login/$', views.loginView.as_view(), name='login'),
    url(r'^newclint/$', views.NewuserViews.as_view(), name='newclint'),
    url(r'^clint/(?P<slug>[\w_-]+)$', views.ClintViews.as_view(), name='clint'),
    url(r'^newaccount/$', views.NewaccountViews.as_view(), name='newaccount'),
    url(r'^accounts/$', views.AccountsViews.as_view(), name='accounts'),
    #url(r'^delaccount/$', views.DelAccountViews.as_view(), name='delaccount'), URL Função Deletar conta para o usuario
    url(r'^account/(?P<pk>[\w_-]+)$', views.AccountViews.as_view(), name='account'),
    url(r'^deposito/$', views.DepositoViews.as_view(), name='deposito'),
    url(r'^saque/$', views.SaqueViews.as_view(), name='saque'),
    url(r'^logout/$', views.ExitView.as_view(), name='sair'),
    url(r'^relatoriogeral/$', views.GeneralReporttView.as_view(), name='generalreportt'),


]