# coding: utf-8

#--------------//////////----------------------

#Projeto Criado por: Lário Diniz
#Contatos: developer.lario@gmail.com
#data: 26/09/2015

#--------------//////////----------------------


from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^$', include('OramaBank.core.urls',namespace='core')),
    url(r'^', include('OramaBank.pynetbanking.urls',namespace='pynetbanking')),
    url(r'^admin_tools/', include('admin_tools.urls')),
    url(r'^admin/', include(admin.site.urls)),
]
