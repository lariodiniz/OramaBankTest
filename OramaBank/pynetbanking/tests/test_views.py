# coding: utf-8

#--------------//////////----------------------

#Projeto Criado por: Lário Diniz
#Contatos: developer.lario@gmail.com
#data: 29/09/2015

#--------------//////////----------------------

from django.test import TestCase
from django.test import Client

from ..models import User, Cliente_Model


class loginViewTest(TestCase):
    def setUp(self):
        self.resp = self.client.get('/login/')

    def test_get(self):
        'Verifica o staus code 200 da pagina /login/'
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        'Verifica o Template Usado'
        self.assertTemplateUsed(self.resp, 'pynetbanking/login.html')

    def test_html(self):
        'Verifica alguns pontos no html do template'
        self.assertContains(self.resp, '<div class="navbar-wrapper"')
        self.assertContains(self.resp, '<form')
        self.assertContains(self.resp, '<input', 4)
        self.assertContains(self.resp, 'type="text"', 2)
        self.assertContains(self.resp, 'type="submit"')

class newclintViewTest(TestCase):
    def setUp(self):
        self.resp = self.client.get('/newclint/')

    def test_get(self):
        'Verifica o staus code 200 da pagina /newclint/'
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        'Verifica o Template Usado'
        self.assertTemplateUsed(self.resp, 'pynetbanking/newclint.html')

    def test_html(self):
        'Verifica alguns pontos no html do template'
        self.assertContains(self.resp, '<div class="navbar-wrapper"')
        self.assertContains(self.resp, '<form')
        self.assertContains(self.resp, '<input', 9)
        self.assertContains(self.resp, 'type="text"', 4)
        self.assertContains(self.resp, 'type="submit"')
"""
class clintViewTest(TestCase):
    def setUp(self):

        obj=User.objects.create(
            username='zezinhio',
            password='12345abc'

        )
        obj.save()
        cliente=Cliente_Model.objects.create(
            user=obj,
            codigo='dasdasdasd',
            cpf='12345678901',
            #slug='zezinhio'
        )
        cliente.save()
        client=Client()
        client.login(username=obj.username, password=obj.password)

        self.resp = self.client.get('/clint/%s' %cliente.slug,secure=True )
        print self.resp
    def test_get(self):
        'Verifica o staus code 200 da pagina /clint/'

        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        'Verifica o Template Usado'
        self.assertTemplateUsed(self.resp, 'pynetbanking/clint.html')

    def test_html(self):
        'Verifica alguns pontos no html do template'
        pass
"""
