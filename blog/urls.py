from django.urls import path
from blog import views

urlpatterns = [
    path('', views.home, name='home'),
    path('blog', views.blog, name='blog'),
    path('blogpost/<str:slug>', views.blogpost, name='blogpost'),
    path('editor', views.editor, name='editor'),
    path('contact', views.contact, name='contact'),
    path('search', views.search, name='search')
]
