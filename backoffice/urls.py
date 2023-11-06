from django.urls import include, path 

from .views import *

urlpatterns = [
    path("", dashboard, name="dashboard"),
    path('users', usersList, name='users'),
    path('users/<int:id>', userDetail, name='user-detail'),
    path('users/<int:id>/', deleteUser, name='delete-user'),
    path('clients', clientsList, name='clients'),
    path('commandes', commandeList, name='commandes'),
    path("login", loginPage, name="login"),
    path("logout", logOutUser, name="logout"),
    path('statistiques', statistiques, name='statistuqes'),


]   
