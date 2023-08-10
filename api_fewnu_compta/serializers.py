from api_fewnu_compta import models
from api_fewnu_compta.models import User
from api_fewnu_compta.models import Customer
from api_fewnu_compta.models import Commande
from api_fewnu_compta.models import Profile
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import *
# User = get_user_model()

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model= User
        fields = ('phone','lastName','firstName','password', 'user_type','adresse')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # return User.objects.create(**validated_data)
        user = User(
            phone=validated_data['phone'],
            firstName=validated_data['firstName'],
            lastName=validated_data['lastName'],
            # email=validated_data['email'],
            adresse = validated_data['adresse']
        )
        user.user_type='owner'
        user.set_password(validated_data['password'])
        user.save()
        return user

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('phone', 'password')

class TokenSerializer(serializers.Serializer):
    """
    This serializer serializes the token data
    """
    token = serializers.CharField(max_length=255)

# for upload file 
class FileUploadSerializer(serializers.Serializer):
    csv_file = serializers.FileField()


# client 
class CustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True, source="createdBy")
    class Meta:
        model = Customer
        fields = ('id', 'nom_complet', 'telephone', 'adresse', 'pays', 'Ville', 'sexe', 'cou', 'epaule', 'longueur_boubou', 'longueur_manche', 'cuisse', 'longueur_pantalon', 'hanche', 'ceinture', 'tour_bras', 'poitrine', 'taille', 'longueur_robe', 'longueur_poitrine', 'bretelle', 'longueur_jupe', 'longueur_haut', 'blouse', 'autre', 'createdBy', 'user','created_at', 'archived')        
# fournisseur 
class FournisseurSerializer(serializers.ModelSerializer):
    # user_id = UserSerializer(read_only=True)
    class Meta:
        model = Fournisseur
        fields =('id','firstName','lastName','telephone','adresse','email','user_id')

# category 
class CategorySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='user')
    class Meta:
        model = Category
        fields =('id','category_name','description','user_id','user')

class ProductSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='user')
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), source='category')
    class Meta:
        model = Product
        fields =('id','libelle','min_stock','qte','prix_achat','prix_vente','image','category_id','user_id','user','category')
        depth = 1

class ArticleSerializer(serializers.ModelSerializer):
    prod_info = ProductSerializer(source="products",read_only=True)
    class Meta:
        model = Article
        fields = ('id','vente','prod_info','products','prod_qte','total')
        # depth = 1

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields ='__all__'
        # depth = 1
        


class VenteSerializer(serializers.ModelSerializer):
    user_info = UserSerializer(source="user",read_only=True)
    client_info = CustomerSerializer(source="client",read_only=True)
    list_products = ArticleSerializer(source='articles', many=True,read_only=True)
    class Meta:
        model = Vente
        fields =('id','user','facture','user_info','client','client_info','list_products','date','status')
        # depth = 1

class DepenseArticleSerializer(serializers.ModelSerializer):
    prod_info = ProductSerializer(source="products",read_only=True)
    class Meta:
        model = DepenseArticle
        fields = ('id','depense','products','prod_info','prod_qte','total')

# depenses 
class DepenseSerializer(serializers.ModelSerializer):
    user_info = UserSerializer(source="user",read_only=True)
    fournisseur_info = CustomerSerializer(source="fournisseur",read_only=True)
    list_products = DepenseArticleSerializer(source='depense_aticle', many=True,read_only=True)
    class Meta:
        model = Depense
        fields =('id','image','matricule','status','user','user_info','fournisseur','fournisseur_info','list_products','date')
        # depth = 1

# paiement
class PaiementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paiement
        fields = '__all__'
        

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'

class AlbumSerializer(serializers.ModelSerializer):
    user = UserSerializer(source="createdBy",read_only=True)

    class Meta:
        model = Album
        fields = ['id', 'name', 'images', 'archived', 'createdBy', 'user']

class PhotoSerializer(serializers.ModelSerializer):
    user = UserSerializer(source="createdBy",read_only=True)
    album = AlbumSerializer(source="albumId",read_only=True)

    class Meta:
        model = Photo
        fields = ['id','albumId','album', 'images', 'createdBy','user' ]


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

class EntreeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True, source='createdBy')
    class Meta:
        model = Entree
        fields = ('id','montant_entree','nom_entree', 'date', 'createdBy', 'user')


class CommandeSerializer(serializers.ModelSerializer):
    numero_commande = serializers.CharField(read_only=True)
    user = UserSerializer(read_only=True, source='createdBy')
    transactions = TransactionSerializer(many=True, read_only=True)  # Modifier cette ligne
    client = CustomerSerializer(read_only=True, source='clientId')
    montant_restant = serializers.SerializerMethodField()
    montant_paye = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Commande
        fields = ('id', 'numero_commande', 'nom_tissu', 'metre_tissu', 'modele', 'date_livraison', 'montant', 'montant_paye', 'montant_restant', 'statut', 'date_commande', 'clientId', 'client', 'createdBy', 'user', 'transactions')

    def create(self, validated_data):
        validated_data['numero_commande'] = Commande.generate_unique_numero_commande()
        return super().create(validated_data)
    
    def get_montant_restant(self, instance):
        transactions = instance.transactions.filter(archived=False)
        montant_paye_total = transactions.aggregate(total=models.Sum('montant_paye'))['total']
        if montant_paye_total is None:
            montant_paye_total = 0
        return instance.montant - montant_paye_total

class CommandeSemaineProchaineSerializer(serializers.ModelSerializer):
     # Modifier cette ligne
    client = CustomerSerializer(read_only=True, source='clientId')
 
    class Meta:
        model = Commande
        fields = ('id', 'modele', 'date_livraison','statut', 'date_commande', 'clientId', 'client')



class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields ='__all__'
        # depth = 1