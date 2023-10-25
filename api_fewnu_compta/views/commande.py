from api_fewnu_compta.serializers import *
from django.db.models import Sum
from rest_framework import generics, permissions, status
from django.utils import timezone
from datetime import timedelta
from rest_framework.response import Response
import io, csv, pandas as pd
from ..models import *
from django.http import HttpResponse
from datetime import datetime, timedelta,date
from rest_framework.parsers import MultiPartParser, FormParser
from django.views.decorators.csrf import csrf_exempt



class CommandeAPIView(generics.ListCreateAPIView):
    """
    POST api/v1/commandes/
    """
    queryset = Commande.objects.all()
    serializer_class = CommandeSerializer
    


    def post(self, request, format=None):
        serializer = CommandeSerializer(data=request.data)
        if serializer.is_valid():
            # print(serializer.data)
            commande = serializer.save()
            commande.save()
            return Response(serializer.data,status=201)
        return Response(serializer.errors, status=400)

    def get(self, request, format=None):
        items = Commande.objects.filter(archived=False).all()
        serializer = CommandeSerializer(items, many=True)
        total_amount = Commande.total_amount()
        # print(total_amount)
        return Response(serializer.data)



class CommandeByIdAPIView(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = (
    #     permissions.IsAuthenticated,
    # )
    queryset = Commande.objects.all()
    serializer_class = CommandeSerializer
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request, id, format=None):
        try:
            item = Commande.objects.filter(archived=False).get(pk=id)
            serializer = CommandeSerializer(item)
            return Response(serializer.data)
        except Commande.DoesNotExist:
            return Response({
                "status": "failure",
                "message": "no such item with this id",
                }, status=404)

    def put(self, request, id, format=None):
        try:
            item = Commande.objects.filter(archived=False).get(pk=id)
        except Commande.DoesNotExist:
            return Response({
                "status": "failure",
                "message": "no such item with this id",
                }, status=404)
        

        # if 'modele' in request.data:
        #     item.image = request.data['modele']
        
        serializer = CommandeSerializer(item, data=request.data, partial= True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    # def delete(self, request, id, format=None):
    def delete(self, request, *args, **kwargs):
        try:
            # today = datetime.now().date()
            # start_of_week = today - timedelta(days=today.weekday())
            # end_of_week = start_of_week + timedelta(days=6)

            # today = datetime.now().date()
            # start_of_next_week = today + timedelta(days=(7 - today.weekday()))
            # end_of_next_week = start_of_next_week + timedelta(days=6)

            item = Commande.objects.filter(archived=False).get(id=kwargs["id"])
        except Commande.DoesNotExist:
            return Response({
                "status": "failure",
                "message": "no such item with this id",
                }, status=404)
        item.archived=True
        item.save()
        return Response({"message": "deleted !"},status=204)


class CommandeByUser(generics.RetrieveAPIView):
    queryset = Commande.objects.all()
    serializer_class = CommandeSerializer

    def get(self, request, id, format=None):
        try:
            # today = timezone.now().date()

            # # Calculer le début et la fin de la semaine en cours (lundi à dimanche)
            # debut_semaine = today - timedelta(days=today.weekday())
            # fin_semaine = debut_semaine + timedelta(days=6)

            today = datetime.now().date()
            start_of_week = today - timedelta(days=today.weekday())
            end_of_week = start_of_week + timedelta(days=6) # Calcul de la fin de la semaine
    
            # commandes_a_livrer = Commande.objects.filter(date_livraison__range=[today, end_of_week])

            commandes_a_livrer_dans_la_semaine = Commande.objects.filter(archived=False,createdBy=id,date_livraison__range=[start_of_week, end_of_week])

            livrer_dans_la_semaine = CommandeCurrenSemaine(commandes_a_livrer_dans_la_semaine, many=True)

            items = Commande.objects.filter(
                archived=False,
                # date_livraison__range=[start_of_week, end_of_week],
                createdBy=id,
                # statut="terminee",
            
            )

            today = datetime.now().date()
            start_of_next_week = today + timedelta(days=(7 - today.weekday()))
            end_of_next_week = start_of_next_week + timedelta(days=6)
   
            commandes_a_livrer_semaine_prochaine = Commande.objects.filter(archived=False,createdBy=id,date_livraison__range=[start_of_next_week, end_of_next_week])
            livrer_semaine_prochaine = CommandeSemaineProchaineSerializer(commandes_a_livrer_semaine_prochaine, many=True)



            today = date.today()
            next_month = today.replace(day=1) + timedelta(days=32)  # Ajoute 32 jours pour être sûr d'aller au mois suivant
            start_of_next_month = next_month.replace(day=1)
            end_of_next_month = start_of_next_month.replace(month=start_of_next_month.month + 1, day=1) - timedelta(days=1)

            commandes_mois_prochain = Commande.objects.filter(archived=False,createdBy=id,date_livraison__range=[start_of_next_month, end_of_next_month])
            livrer_mois_prochain = CommandeMoisProchainSerializer(commandes_mois_prochain, many=True)

   
            serializer = CommandeSerializer(items, many=True)
            clients = Customer.objects.filter(commande__in=items).distinct()

            # Liste pour stocker les informations des clients avec les avances
            clients_info = []

            for client in clients:
                client_info = {
                    'client': CustomerSerializer(client).data,
                    'total_avance': items.filter(clientId=client).aggregate(Sum('montant'))['montant__sum'],
                }
                clients_info.append(client_info) 

            prix_total = 0  # Calcul du prix total initial
            total_montant_avance = 0
            total_montant_restant = 0
            for obj in serializer.data:
                total_montant_avance += float(obj['montant_paye'])
                prix_total += obj['montant']  # Ajout du montant de chaque objet pour calculer le prix total
                total_montant_restant = prix_total - total_montant_avance
                obj['prixTotal'] = prix_total  # Ajout de la clé "prixTotal" à chaque objet
                obj['TotalAvance'] = total_montant_avance  # Ajout de la clé "TotalAvance" à chaque objet
                obj['totalRestant'] = obj['montant'] - float(obj['montant_paye'])  # Calcul du montant restant correct
                
        
            response_data = {
                'prixTotal': prix_total, 
                'TotalAvance':total_montant_avance,
                'totalRestant' : total_montant_restant,
                "total_commandes": items.count(),
                'data': serializer.data,
                'clients': clients_info,
                # "commandes_a_livrer":commandes_a_livrer
                "livrer_semaine_prochaine":livrer_semaine_prochaine.data,
                'livrer_mois_prochain': livrer_mois_prochain.data,
                'livrer_dans_la_semaine': livrer_dans_la_semaine.data,
                
                }
            # print(total_montant_restant)
            return Response(response_data)
        except Commande.DoesNotExist:
            return Response({
                "status": "failure",
                "message": "no such item with this id",
            }, status=404)











