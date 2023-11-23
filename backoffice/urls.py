from django.urls import include, path 

from .views import *

urlpatterns = [
    path("", dashboard, name="dashboard"),
    path('users', usersList, name='users'),
    path('users/<int:id>', userDetail, name='user-detail'),
    path('users/<int:id>/', deleteUser, name='delete-user'),
    path('bloc_user/<int:id>/', blocUser, name='bloc_user'),
    path('dbloc_user/<int:id>/', dblocUser, name='bloc_user'),

    path('clients', clientsList, name='clients'),
    path('commandes', commandeList, name='commandes'),
    path('statistiques', statistiques, name='statistuqes'),
    # path('get_user_data/', get_user_data, name='get_user_data'),

    path("login", loginPage, name="login"),
    path("logout", logOutUser, name="logout")

]   
