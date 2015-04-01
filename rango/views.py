# -*- coding: utf-8 -*-
from django.shortcuts import render
# from django.http import HttpResponse


def index(request):

    # Construir um dicionário para passar para o motor do template
    # como seu contexto.
    # Note que a chave boldmessage é a mesma {{ boldmessage }} no template!
    context_dict = {'boldmessage': 'Eu sou a fonte em negrito do contexto.'}

    # Retorna uma resposta (response) renderizada para enviar ao cliente.
    # Nós usamos a função atalho para tornar nosso trabalho mais fácil.
    # Note que o primeiro parâmetro é o template que desejamos usar.
    return render(request, 'rango/index.html', context_dict)


def about(request):
    context_dict = {'message': 'Not necessary'}
    return render(request, 'rango/about.html', context_dict)
