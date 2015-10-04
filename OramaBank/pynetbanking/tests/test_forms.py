# coding: utf-8

#--------------//////////----------------------

#Projeto Criado por: Lário Diniz
#Contatos: developer.lario@gmail.com
#data: 29/09/2015

#--------------//////////----------------------

from django.test import TestCase

from ..forms import LoginForm,NewclintForm, AccountForm, OperacaoForm
from..models import Cliente_Model

class LoginFormTest(TestCase):
    def test_has_fields(self):
        'Form tem 2 campos'
        form= LoginForm()
        self.assertItemsEqual(['username', 'password'], form.fields)

class NewclintFormTest(TestCase):
    def test_has_fields(self):
        'form tem 7 campos'
        form = NewclintForm()
        self.assertItemsEqual(['username','first_name','last_name','email','password', 'confirm_the_password', 'cpf'], form.fields)


class AccountFormTest(TestCase):
    def test_has_fields(self):
        'form tem 2 campos'
        form = AccountForm()
        self.assertItemsEqual(['saldo','tipo'], form.fields)

class OperacaoFormTest(TestCase):
    def test_has_fields(self):
        'form tem 2 campos'
        form = OperacaoForm()
        self.assertItemsEqual(['valor'], form.fields)


