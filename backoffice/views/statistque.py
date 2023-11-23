from django.shortcuts import render, redirect
from api_fewnu_compta.models import User,Customer,Commande
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from datetime import datetime, timedelta
from django.db.models import Count
from django.db.models.functions import TruncMonth,TruncWeek,TruncDate
from django.utils import timezone
from django.db.models.functions import ExtractWeek,ExtractMonth




def is_admin(user):
    return user.is_authenticated and user.is_superuser

@login_required
@user_passes_test(is_admin)
def statistiques(request):
    active_users = User.objects.filter(is_active=True)

 
    user_registration_data = User.objects.annotate(date=TruncDate('date_joined')).values('date').annotate(count=Count('id')).order_by('-date')
    labels = [entry['date'].strftime('%Y-%m-%d') for entry in user_registration_data]
    data = [entry['count'] for entry in user_registration_data]

    user_registration_data_by_month = User.objects.annotate(month=TruncMonth('date_joined')).values('month').annotate(count=Count('id')).order_by('-month')
    labelsMonth = [entry['month'].strftime('%Y-%m') for entry in user_registration_data_by_month]
    dataMonth = [entry['count'] for entry in user_registration_data_by_month]

    user_registration_dataByWeek = User.objects.annotate(week=TruncWeek('date_joined')).values('week').annotate(count=Count('id')).order_by('-week')
    labelsWeek = [entry['week'].strftime('%Y-%U') for entry in user_registration_dataByWeek]
    dataWeek = [entry['count'] for entry in user_registration_dataByWeek]

    "===============================================Nombre de user actif par mois=========================="
    active_users_by_month = []

    # Récupérer les données d'utilisateurs actifs par mois
    active_users = User.objects.filter(is_active=True)
    for user in active_users:
        # Récupérer le nombre de clients ajoutés par l'utilisateur par mois
        clients_added_by_month = (
            Customer.objects.filter(createdBy=user)
            .annotate(month=ExtractMonth('created_at'))
            .values('month')
            .annotate(count=Count('id'))
        )

        # Vérifier le nombre de clients ajoutés par mois
        for month in clients_added_by_month:
            if month['count'] <= 20:

                active_users_by_month.append(user.id)


    active_users_month = len(set(active_users_by_month))
    # print("=============> ", active_users_month)





    "===================================Nombre de user actifs par semaine================================="

    active_users_by_week = []

    for user in active_users:
        # Récupérer le nombre de clients ajoutés par l'utilisateur par semaine
        clients_added_by_week = (
            Customer.objects.filter(createdBy=user)
            .annotate(week=ExtractWeek('created_at'))
            .values('week')
            .annotate(count=Count('id'))
        )
        for week in clients_added_by_week:
                if week['count'] <= 10:
                    active_users_by_week.append(user.id)

   

    active_users_wee = len(set(active_users_by_week))

    print('=====================week',active_users_wee)




    "==============================Nombre de user actif par jour=========================================="
    
    users_with_five_clients_per_day = []


    clients_added_per_day_by_user = {}
    for user in active_users:
        # Obtenez la liste des clients ajoutés par cet utilisateur pour chaque jour
        clients_added_by_day = (
            Customer.objects.filter(createdBy=user, created_at__date=timezone.now())
            .values('created_at__date')
            .annotate(count=Count('id'))
        )
        clients_added_per_day_by_user[user.id] = clients_added_by_day

        # print(clients_added_per_day_by_user[user.id])
        for day in clients_added_by_day:
            if day['count'] <= 5:
                users_with_five_clients_per_day.append(user)

    active_users_count = len(set(users_with_five_clients_per_day))

    print('=====================',active_users_count)



    context = {
        'labels': labels,
        'data': data,
        'labelsWeek': labelsWeek,
        'dataWeek': dataWeek,
        'labelsMonth': labelsMonth,
        'dataMonth': dataMonth,
        'active_users_count': active_users_count,
        'active_users_wee': active_users_wee,
        'active_users_month': active_users_month,

    }
    return render(request, "backoffice/statistiques.html", context)




