from django.shortcuts import render, redirect
from api_fewnu_compta.models import User,Customer,Commande
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages



def is_admin(user):
    return user.is_authenticated and user.is_superuser

@login_required
@user_passes_test(is_admin)
def usersList(request):
    users = User.objects.all().order_by("-id")
    context = {"users":users}
    return render(request, "backoffice/users/userList.html", context)



@login_required
@user_passes_test(is_admin)
def userDetail(request, id):
    user = User.objects.get(id=id)
    num_clients = Customer.objects.filter(createdBy=user).count()
    num_commandes = Commande.objects.filter(createdBy=user).count()
    clients = Customer.objects.filter(createdBy=user)
    commandes = Commande.objects.filter(createdBy=user)
    clients_dates_ajout = [client.created_at for client in clients]
    commandes_dates_ajout = [commande.date_commande for commande in commandes]

    num_clients = len(clients)
    num_commandes = len(commandes)
    clients_dates_str = ", ".join([str(date) for date in clients_dates_ajout])
    commandes_dates_str = ", ".join([str(date) for date in commandes_dates_ajout])
    clients_dates_list = clients_dates_ajout
    commandes_dates_list = commandes_dates_ajout


    context = {"user":user, "num_clients":num_clients, "num_commandes":num_commandes, "clients_dates_ajout":clients_dates_list, "commandes_dates_ajout":commandes_dates_list}

    return render(request, "backoffice/users/userDetail.html",  context)


@login_required
@user_passes_test(is_admin)
def deleteUser(request, id):
        user = User.objects.filter(archived=False).get(id=id)
        if request.method == "POST":
            user.archived =True
            user.save()
            messages.success(request, "Utilisateur " + user.firstName + " supprime avec success ")
            return redirect('users')
        context = {"user":user}
        return render(request, 'backoffice/users/deleteUser.html', context)
