from django.urls import path
from blog import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register', views.register, name='register'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name="logout"),
    path('blog', views.blog, name='blog'),
    path('blogpost/<str:slug>', views.blogpost, name='blogpost'),
    path('editor', views.editor, name='editor'),
    path('editpost/<str:slug>', views.editpost, name='editpost'),
    path('deletepost/<str:slug>', views.deletepost, name='deletepost'),
    path('contact', views.contact, name='contact'),
    path('profile', views.profile, name='profile'),
    path('search', views.search, name='search')
] 
