from api_fewnu_compta.serializers import *
from rest_framework import generics, permissions, status
from rest_framework.response import Response
import io, csv, pandas as pd
from ..models import Commande
from django.http import HttpResponse
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
        print(total_amount)
        return Response(serializer.data)



class CommandeByIdAPIView(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = (
    #     permissions.IsAuthenticated,
    # )
    queryset = Commande.objects.all()
    serializer_class = CommandeSerializer

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
        self.data = request.data.copy()        
        serializer = CommandeSerializer(item, data= self.data, partial= True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    # def delete(self, request, id, format=None):
    def delete(self, request, *args, **kwargs):
        try:
            item = Commande.objects.filter(archived=False).get(id=kwargs["id"])
        except Commande.DoesNotExist:
            return Response({
                "status": "failure",
                "message": "no such item with this id",
                }, status=404)
        item.archived=True
        item.save()
        return Response({"message": "deleted"},status=204)


class CommandeByUser(generics.RetrieveAPIView):
    queryset = Commande.objects.all()
    serializer_class = CommandeSerializer

    def get(self, request, id, format=None):
        try:
            item = Commande.objects.filter(archived=False).filter(createdBy=id)
            serializer = CommandeSerializer(item, many=True)
            prix_total = 0  # Calcul du prix total initial
            for obj in serializer.data:
                prix_total += obj['montant']  # Ajout du montant de chaque objet pour calculer le prix total
                obj['prixTotal'] = prix_total  # Ajout de la clé "prixTotal" à chaque objet

            response_data = {'prixTotal': prix_total, 'data': serializer.data}
            return Response(response_data)
        except Commande.DoesNotExist:
            return Response({
                "status": "failure",
                "message": "no such item with this id",
            }, status=404)








