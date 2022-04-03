from django.urls import path, re_path
from django.views.decorators.cache import cache_page

from .views import (
    WomenHome, WomenCategory, ShowPost, about, AddPost, ContactFormView, LoginUser, RegisterUser,
    logout_user
)


urlpatterns = [
    path('', WomenHome.as_view(), name='home'),
    path('post/<str:slug>/', ShowPost.as_view(), name='post'),
    path('category/<str:slug>/', WomenCategory.as_view(), name='category'),
    path('about/', about, name='about'),
    path('add-post/', cache_page(60*15)(AddPost.as_view()), name='add_post'),
    path('contact/', ContactFormView.as_view(), name='contact'),
    path('login/', LoginUser.as_view(), name='login'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('logout/', logout_user, name='logout'),
]
