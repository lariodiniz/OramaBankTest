# coding: utf-8

#--------------//////////----------------------

#Projeto Criado por: Lário Diniz
#Contatos: developer.lario@gmail.com
#data: 26/09/2015

#--------------//////////----------------------

from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from .models import Cliente_Model, Conta_Model
from django.contrib.auth import authenticate

from localflavor.br.forms import BRCPFField


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username','password')

    def __init__(self, *args, **kwargs):
        #configuração username
        self.base_fields['username'].help_text = ''
        #self.base_fields['username'].type =_('text')
        self.base_fields['username'].label =_('Nome')

        #configurando password

        self.base_fields['password'].widget = forms.PasswordInput()
        self.base_fields['password'].label =_('Senha')
        #self.base_fields['password'].type =_('password')


        super(LoginForm, self).__init__(*args, **kwargs)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        user = authenticate(username=username, password=password)
        if not user or not user.is_active:
            raise forms.ValidationError("Desculpe, Este Login é invalido. tente Novamente.")
        return self.cleaned_data

    def login(self, request):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        return user


    def get_absolute_url(name):
        return reverse('personagens', kwargs={'name': name})

class NewclintForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username','first_name','last_name','email','password')

    confirm_the_password=forms.CharField(label=_('Confirme a Senha'), max_length=30, widget=forms.PasswordInput, help_text = 'Repita a mesma senha')
    cpf=BRCPFField()

    def __init__(self, *args, **kwargs):

        #configuração username
        self.base_fields['username'].help_text = 'Somente letras, dígitos e @/./+/-/_.'
        self.base_fields['username'].label =_('Nome')
        #self.base_fields['class'] =_('text')


        #configurando first_name
        self.base_fields['first_name'].label =_('Primeiro Nome')
        #elf.base_fields['first_name'].type =_('text')

        #configurando last_name
        self.base_fields['last_name'].label =_('Sobrenome')
        #self.base_fields['last_name'].type =_('text')

        #configurando email
        self.base_fields['email'].label =_('Email')
        #self.base_fields['email'].type =_('text')

        #configurando password
        self.base_fields['password'].help_text = 'Informe uma senha segura'
        self.base_fields['password'].widget = forms.PasswordInput()
        self.base_fields['password'].label =_('Senha')
        #self.base_fields['password'].type =_('password')

        super(NewclintForm, self).__init__(*args, **kwargs)


    def clean_confirm_the_password(self):
        if self.cleaned_data['confirm_the_password'] != self.data['password']:
            raise forms.ValidationError('Confirmacao da senha nao confere!')
        return self.cleaned_data['confirm_the_password']


    def save(self, commit=True):
        usuario = super(NewclintForm, self).save(commit=False)
        usuario.set_password(self.cleaned_data['password'])
        if commit:
            usuario.save()
            n=str()
            for x in range(10):
                n+=str(random.randrange(0,9))

            Cliente_Model.objects.create(
            user=usuario,
            cpf=self.cleaned_data['cpf'],
            codigo=n)
        return usuario


class AccountForm(forms.ModelForm):

    class Meta:
        model= Conta_Model
        fields = ('saldo','tipo')

    def __init__(self, *args, **kwargs):

        #configuração saldo
        self.base_fields['saldo'].help_text = 'Deposito Inicial'
        self.base_fields['saldo'].label =_('Saldo')

        #configuração Tipo
        self.tipo_choices = kwargs.pop('tipo_choices', None)
        super(AccountForm,self).__init__(*args,**kwargs)
        self.fields['tipo'].queryset = self.tipo_choices


class OperacaoForm(forms.Form):
    valor = forms.FloatField(label=_('Valor'))



