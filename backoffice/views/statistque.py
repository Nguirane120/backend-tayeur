from django.shortcuts import render, redirect
from api_fewnu_compta.models import User,Customer,Commande
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from datetime import datetime, timedelta
from django.db.models import Count
from django.db.models.functions import TruncMonth,TruncWeek



def is_admin(user):
    return user.is_authenticated and user.is_superuser

@login_required
@user_passes_test(is_admin)
def statistiques(request):
    today = datetime.now().date()

    one_week_ago = today - timedelta(days=1)
    one_month_ago = today - timedelta(days=90)
    three_months_ago = today - timedelta(days=90)  # Nouvelle période de 3 mois


    users_by_day = User.objects.filter(date_joined__gte=today).values('date_joined').annotate(count=Count('id'))

    users_by_week = User.objects.filter(date_joined__gte=one_week_ago).values('date_joined').annotate(
        month=TruncWeek('date_joined')).annotate(count=Count('id'))

    users_by_month = User.objects.filter(date_joined__gte=one_month_ago).annotate(
        month=TruncMonth('date_joined')
    ).values('month').annotate(count=Count('id'))

    
    user_day_length = len(users_by_day)

    
    user_week_length = len(users_by_week)
    
    # user_dates_ajout = [commande.date_commande for commande in commandes]


    context = {"users_by_day":users_by_day,"users_by_week":users_by_week,"users_by_month":users_by_month,"today": today,
        "one_week_ago": one_week_ago,
        "one_month_ago": one_month_ago,"user_day_length":user_day_length,"user_week_length":user_week_length}
    return render(request, "backoffice/statistiques.html", context)




