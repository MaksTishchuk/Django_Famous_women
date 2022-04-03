from django.contrib.auth import logout, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView

from .models import Women, Category
from .forms import AddPostForm, RegisterUserForm, LoginUserForm, ContactForm
from .utils import *


class WomenHome(DataMixin, ListView):
    """Представление для вывода всех постов"""

    paginate_by = 2
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Women.objects.filter(is_published=True).select_related('category')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        add_context = self.get_user_context(title='Main Page')
        context.update(add_context)
        return context


class WomenCategory(DataMixin, ListView):
    """Представление для вывода постов по категориям"""

    paginate_by = 2
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Women.objects.filter(
            category__slug=self.kwargs['slug'], is_published=True
        ).select_related('category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = Category.objects.get(slug=self.kwargs['slug'])
        add_context = self.get_user_context(
            title=str(category.name),
            cat_selected=category.id
        )
        context.update(add_context)
        return context


class ShowPost(DataMixin, DetailView):
    """Представление для полного отображения поста"""

    model = Women
    template_name = 'women/post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        add_context = self.get_user_context(title=context['post'].title, cat_selected='-')
        context.update(add_context)
        return context


def about(request):
    """Страничка - О сайте"""

    categories = Category.objects.annotate(Count('women'))

    return render(
        request,
        'women/about.html',
        {'title': 'О сайте', 'menu': menu, 'cat_selected': '-', 'categories': categories}
    )


class AddPost(LoginRequiredMixin, DataMixin, CreateView):
    """Представление добавления поста"""

    form_class = AddPostForm
    template_name = 'women/add_post.html'
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        add_context = self.get_user_context(title='Добавление статьи', cat_selected='-')
        context.update(add_context)
        return context


class ContactFormView(DataMixin, FormView):
    """Представление обратной связи"""

    form_class = ContactForm
    template_name = 'women/contact.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        add_context = self.get_user_context(title='Обратная связь', cat_selected='-')
        context.update(add_context)
        return context

    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect('home')


class RegisterUser(DataMixin, CreateView):
    """Представление для регистрации пользователей"""

    form_class = RegisterUserForm
    template_name = 'women/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        add_context = self.get_user_context(title='Регистрация', cat_selected='-')
        context.update(add_context)
        return context

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    """Представление для регистрации пользователей"""

    form_class = LoginUserForm
    template_name = 'women/login.html'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        add_context = self.get_user_context(title='Авторизация', cat_selected='-')
        context.update(add_context)
        return context

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')


def page_not_found(request, exception):
    """Функция для обработки запроса, если страница не найдена"""

    return HttpResponseNotFound('<h1>Страница не найдена!</h1>')
