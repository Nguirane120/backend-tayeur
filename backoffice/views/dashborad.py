from django.shortcuts import render
from django.http import HttpResponse
from api_fewnu_compta.models import *
from django.template import loader
# from ..decorators import  unauthenticated_user, allowed_user
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required, user_passes_test
from datetime import datetime, timedelta
from django.db.models.functions import TruncDay, TruncWeek
from django.db.models import Count

def is_admin(user):
    return user.is_authenticated and user.is_superuser

@login_required
@user_passes_test(is_admin)
def dashboard(request):
    template = loader.get_template("backoffice/dashboard.html")
    users = User.objects.all().count()
    clients = Customer.objects.all().count()
    commandes = Commande.objects.all().count()
    albums = Album.objects.all().count()
    transactions = Transaction.objects.all().count()
    entrees = Entree.objects.all().count()

    one_week_ago = datetime.now() - timedelta(days=7)
    daily_customer_count = Customer.objects.filter(created_at__gte=one_week_ago).annotate(
    day=TruncDay('created_at')
).values('day', 'createdBy__firstName').annotate(count=Count('id'))
    
    today = datetime.now().date()
    start_of_week = today - timedelta(days=today.weekday())

# Date de fin de la semaine
    end_of_week = start_of_week + timedelta(days=6)   
    weekly_customer_count = Customer.objects.filter(created_at__range=(start_of_week, end_of_week)
).annotate(
    week=TruncWeek('created_at')
).values('week', 'createdBy__firstName').annotate(count=Count('id'))

    context = {"users":users, 
               "clients":clients, 
               "commandes":commandes, 
               "transactions":transactions, 
               "entrees":entrees, 
               "albums":albums,
               "daily_customer_count":daily_customer_count,
               "weekly_customer_count":weekly_customer_count,
               }
    return render(request, "backoffice/dashboard.html", context)
    # return HttpResponse(template.render(context, request))