# -*- coding: utf-8 -*-
from django import forms
from rango.models import Page, Category, UserProfile
from django.contrib.auth.models import User


class CategoryForm(forms.ModelForm):
    name = forms.CharField(
        max_length=128,
        help_text='Insira o nome da categoria'
    )
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    # Uma classe aninhada para fornecer info adicional ao model
    class Meta:
        model = Category
        fields = ('name',)


class PageForm(forms.ModelForm):
    title = forms.CharField(
        max_length=128,
        help_text='Insira o título da página'
    )
    url = forms.URLField(max_length=200, help_text='Insira a URL da página')
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        model = Page
        exclude = ('category',)

    def clean(self):
        url = self.cleaned_data.get('url')
        # Se a url não está vazia e não inicia com http://, adicionamos
        if url and not url.startswith('http://'):
            url = 'http://' + url
            self.cleaned_data['url'] = url
        return self.cleaned_data


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website', 'picture')
