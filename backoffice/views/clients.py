from django.shortcuts import render
from api_fewnu_compta.models import Customer
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required, user_passes_test
from datetime import datetime, timedelta
from django.db.models.functions import TruncDay
from django.db.models import Count




def is_admin(user):
    return user.is_authenticated and user.is_superuser

@login_required
@user_passes_test(is_admin)
def clientsList(request):
    clients = Customer.objects.all().order_by("-id")
    context = {"clients":clients}
    return render(request, "backoffice/clients/clientsList.html", context)

@login_required
@user_passes_test(is_admin)
def nombre_client_par_jour(request):
    one_week_ago = datetime.now() - timedelta(days=7)
    daily_customer_count = Customer.objects.filter(created_at__gte=one_week_ago).annotate(
    day=TruncDay('created_at')
).values('day', 'createdBy__username').annotate(count=Count('id'))
    context = {"daily_customer_count":daily_customer_count}

    return render(request, "backoffice/clients/nombre_client_par_mois.html", context)
