from django.db import models
from django.db.models import Max
from django.utils import timezone
from .user import User
from .client import Customer
from .transaction import Transaction


NOUVELLE = 'nouvelle'
LIVREE = 'livree'
ENCOURS = 'encours'
TERMINEE = 'terminee'
STATUS_TYPES = (
    (NOUVELLE, 'Nouvelle'),
    (LIVREE, 'Livree'),
    (ENCOURS, 'Encours'),
    (TERMINEE, 'Terminee'),
)


class Commande(models.Model):
    nom_tissu = models.CharField(max_length=255, null=True, blank=True)
    metre_tissu = models.IntegerField(null=True, blank=True)
    modele = models.FileField(upload_to='images/', blank=True, null=True)
    date_livraison = models.DateTimeField(default=timezone.now, blank=True, null=True)
    montant = models.FloatField()
    statut = models.CharField(max_length=300, choices=STATUS_TYPES, null=True, blank=True, default=NOUVELLE)
    clientId = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    createdBy = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    archived = models.BooleanField(default=False)
    date_commande = models.DateTimeField(default=timezone.now)
    numero_commande = models.CharField(max_length=4, unique=True)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='commandes', null=True, blank=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._montant_restant = None  # Valeur par défaut pour montant_restant lors de la création

    "hello"
    def update_montant_restant(self):
        transactions = self.transactions.filter(archived=False)
        montant_paye_total = transactions.aggregate(total=models.Sum('montant_paye'))['total']
        if montant_paye_total is None:
            montant_paye_total = 0
        self._montant_restant = self.montant - montant_paye_total
        # print(self._montant_restant)

    def update_avance(self):
        transactions = self.transactions.filter(archived=False)
        self.avance = transactions.aggregate(total=models.Sum('montant_paye'))['total'] or 0

    def __str__(self):
        return f'{str(self.nom_tissu)}'

    def save(self, *args, **kwargs):
        if not self.pk:
            self.numero_commande = Commande.generate_unique_numero_commande()
        super().save(*args, **kwargs)
        self.update_montant_restant()
        self.update_avance()

    @staticmethod
    def generate_unique_numero_commande():
        last_numero = Commande.objects.all().aggregate(Max('numero_commande'))['numero_commande__max']
        if last_numero:
            new_numero = str(int(last_numero) + 1).zfill(4)
        else:
            new_numero = '0001'
        return new_numero


    def montant_paye(self):
        transactions = self.transactions.filter(archived=False)
        montant_paye_total = transactions.aggregate(total=models.Sum('montant_paye'))['total']
        if montant_paye_total is None:
            montant_paye_total = 0
        return montant_paye_total

    def montant_restant(self):
        if self._montant_restant is None:
            return None
        return self._montant_restant

    def avance(self):
        transactions = self.transactions.filter(archived=False)
        avance = transactions.aggregate(total=models.Sum('montant_paye'))['total']
        if avance is None:
            avance = 0
        return avance
    
# les montants globaux
    @classmethod
    def total_amount(cls):
        return cls.objects.aggregate(models.Sum('montant'))['montant__sum']
    

