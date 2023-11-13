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



def is_admin(user):
    return user.is_authenticated and user.is_superuser

@login_required
@user_passes_test(is_admin)
def statistiques(request):
 
    user_registration_data = User.objects.annotate(date=TruncDate('date_joined')).values('date').annotate(count=Count('id'))
    labels = [entry['date'].strftime('%Y-%m-%d') for entry in user_registration_data]
    data = [entry['count'] for entry in user_registration_data]

    user_registration_data_by_month = User.objects.annotate(month=TruncMonth('date_joined')).values('month').annotate(count=Count('id'))
    labelsMonth = [entry['month'].strftime('%Y-%m') for entry in user_registration_data_by_month]
    dataMonth = [entry['count'] for entry in user_registration_data_by_month]

    user_registration_dataByWeek = User.objects.annotate(week=TruncWeek('date_joined')).values('week').annotate(count=Count('id'))
    labelsWeek = [entry['week'].strftime('%Y-%U') for entry in user_registration_dataByWeek]
    dataWeek = [entry['count'] for entry in user_registration_dataByWeek]



    context = {
        'labels': labels,
        'data': data,
        'labelsWeek': labelsWeek,
        'dataWeek': dataWeek,
        'labelsMonth': labelsMonth,
        'dataMonth': dataMonth,
    }
    return render(request, "backoffice/statistiques.html", context)




