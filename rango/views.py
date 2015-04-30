# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm


def index(request):

    # Consulte o banco de dados por uma lista de TODAS as categorias.
    # Ordene as categorias pelo número de likes em ordem decrescente.
    # Recupere apenas o top 5- ou todas se for menos do que 5
    pages = Page.objects.order_by('-views')[:5]
    categories = Category.objects.order_by('-likes')[:5]
    context_dict = {'categories': categories}
    context_dict['pages'] = pages

    # Renderize a resposta e envie-a de volta
    return render(request, 'rango/index.html', context_dict)


def about(request):
    context_dict = {'message': 'Not necessary'}
    return render(request, 'rango/about.html', context_dict)


def category(request, category_name_slug):
    # Crie um dicionário de contexto para que possamos passar para engine
    # de renderização de template.
    context_dict = {}
    try:
        # Nós podemos encontrar um slug do nome da categoria com o nome dado
        # Se não encontrarmos, o método .get()  lança uma exceção DoesNotExist
        # Assim, o método .get() retorna 1 instância do model ou lança exceção
        category = Category.objects.get(slug=category_name_slug)
        context_dict['category_name'] = category.name

        # Recupera todas as páginas associadas.
        # Note que o filter retorna >= 1 instância de model.
        pages = Page.objects.filter(category=category)

        # Adicione nossa lista de resultados de contexto com o nome 'pages'
        context_dict['pages'] = pages
        # Nós também adicionamos o objeto category do banco para o contexto.
        # Usaremos isso no template para verificar se a categoria existe
        context_dict['category'] = category
    except Category.DoesNotExist:
        # Entramos aqui se não tiver sido encontrada a categoria desejada
        # Não faça nada - o template mostrará a mensagem "sem categoria".
        pass
    # Renderize a resposta e retorne-a para o cliente.
    context_dict['category_name_slug'] = category_name_slug
    return render(request, 'rango/category.html', context_dict)


@login_required
def add_category(request):
    # É um POST HTTP?
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        # O form é válido?
        if form.is_valid():
            # Salve a nova categoria no banco
            form.save(commit=True)
            # Agora chame a view index()
            # O usuário será levado para a página inicial
            return index(request)
        else:
            # O form fornecido contém erros - dê print neles
            print form.errors
    else:
        # Se a requisição não é POST, mostre o form para inserir dados
        form = CategoryForm()

    # Renderize o form com as mensagens de erro (se houver alguma)
    return render(request, 'rango/add_category.html', {'form': form})


@login_required
def add_page(request, category_name_slug):
    try:
        cat = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        cat = None
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if cat:
                page = form.save(commit=False)
                page.category = cat
                page.views = 0
                page.save()
                return category(request, category_name_slug)
        else:
            print form.errors
    else:
        form = PageForm()
    context_dict = {'form': form, 'category': cat}
    return render(request, 'rango/add_page.html', context_dict)


def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    return render(
        request,
        'rango/register.html',
        {
            'user_form': user_form,
            'profile_form': profile_form,
            'registered': registered
        }
    )


def user_login(request):
    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/rango/')
            else:
                return HttpResponse('Sua conta está desativada.')
        else:
            print("Detalhes inválidos de login: {0}, {1}".format(
                username, password)
            )
            context_dict = {'errors': 'Nome de user ou senha incorretos.'}
            return render(request, 'rango/login.html', context_dict)
            # return HttpResponse("Detalhes inválidos de login fornecidos.")
    else:
        return render(request, 'rango/login.html', {})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/rango/')


@login_required
def restricted(request):
    return render(request, 'rango/restricted.html', {})
