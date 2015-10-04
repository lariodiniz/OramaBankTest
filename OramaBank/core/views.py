# coding: utf-8

#--------------//////////----------------------

#Projeto Criado por: Lário Diniz
#Contatos: developer.lario@gmail.com
#data: 26/09/2015

#--------------//////////----------------------

from django.views.generic import TemplateView

class IndexView(TemplateView):
    template_name = "core/index.html"
