# coding: utf-8

#--------------//////////----------------------

#Projeto Criado por: Lário Diniz
#Contatos: developer.lario@gmail.com
#data: 29/09/2015

#--------------//////////----------------------

from django.test import TestCase

class IndexViewTest(TestCase):
    def setUp(self):
        self.resp = self.client.get('/')

    def test_get(self):
        'Verifica o staus code 200 da pagina inicial'
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        'Verifica o Template Usado'
        self.assertTemplateUsed(self.resp, 'core/index.html')

    def test_html(self):
        'Verifica alguns pontos no html do template'
        self.assertContains(self.resp, '<div class="navbar-wrapper"')
        self.assertContains(self.resp, 'class="carousel slide"')
