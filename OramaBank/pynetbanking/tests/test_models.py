# coding: utf-8

#--------------//////////----------------------

#Projeto Criado por: Lário Diniz
#Contatos: developer.lario@gmail.com
#data: 26/09/2015

#--------------//////////----------------------

from django.test import TestCase

from django.utils import timezone


from ..models import Cliente_Model,Conta_Model,Operacao_model,User

class Cliente_ModelTest(TestCase):
    def setUp(self):
        self.obj=User.objects.create(
            username='Zézinho',
            password='12345abc'

        )
        self.obj.save()
        Cliente_Model.objects.create(
            user=self.obj,
            codigo='dasdasdasd',
            cpf='12345678901'

        ).save()
    def test_create(self):
        "Cliente_model precisa ter User, Código e cpf "

        self.assertEqual(1, self.obj.pk)
        self.assertIsInstance(self.obj.cliente_model, Cliente_Model)

class Conta_ModelTest(TestCase):
    def setUp(self):
        self.obj=User.objects.create(
            username='Zézinho',
            password='12345abc'

        )
        self.obj.save()
        self.conta=Conta_Model.objects.create(
            user=self.obj,
            data=timezone.now(),
            saldo=200.00,
            tipo='Conta Corrente'

        )

        self.conta.save()
    def test_create(self):
        "Conta model precisa ter User, data, saldo e tipo "

        self.assertEqual(1, self.conta.pk)
        self.assertIsInstance(self.conta.user, User)


class Operacao_ModelTest(TestCase):
    def setUp(self):
        self.obj=User.objects.create(
            username='Zézinho',
            password='12345abc'

        )
        self.obj.save()
        self.conta=Conta_Model.objects.create(
            user=self.obj,
            data=timezone.now(),
            saldo=200.00,
            tipo='Conta Corrente'

        )

        self.conta.save()
    def test_create(self):
        "Faz uma operação e verifica o histórico no Modelo Operacao_model e o saldo da conta"
        self.conta.operacao('saque', 50.00)
        self.assertEqual(Operacao_model.objects.get(conta=self.conta.pk).conta.pk, self.conta.pk)
        self.assertEqual(Operacao_model.objects.get(conta=self.conta.pk).valor, 50.00)
        self.assertEqual(Operacao_model.objects.get(conta=self.conta.pk).tipo, 'saque')
        self.assertEqual(self.conta.saldo, 150.00)
