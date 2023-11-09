from django.contrib import admin
from django.conf import settings 
from django.urls import path, include

from drf_yasg import openapi
from drf_yasg.views import get_schema_view as swagger_get_schema_view
from . import views
from django.conf.urls.static import static 
from .views.employee import *
from .views.paiement import * 
# from .views import SendTwilioMessageView
# from ..gestion_horaire.views import *
schema_view = swagger_get_schema_view(
    openapi.Info(
        title="Tayeur Gestion",
        default_version='1.0.0',
        description="API documentation of Tayeur Gestion",
    ),
    public=True,
)

urlpatterns = [
    path('v1/', 
        include([

            # authentification 
            path('login/', views.LoginView.as_view()),
            path('logout/', views.logout_view),
            path('csrftoken', views.GetCSRFToken.as_view()),

            # path('reset-password/verify-token/', views.CustomPasswordTokenVerificationView.as_view(), name='password_reset_verify_token'),
            # path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),

            # user 
            path('users/', views.UserAPIView.as_view()),
            path('users/<int:id>', views.UserById.as_view()),
            path('users/password/<int:id>', views.UserUpdatePassword.as_view()),
            path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name="swagger-schema"),

            # clients 
       
            path('clients',views.CustomerAPIView.as_view()),
            path('clients/upload',views.CustomerUploadFileView.as_view()),
            path('clients/export',views.CustomerExportFileView),
            path('clients/<int:id>/',views.CustomerByIdAPIView.as_view()),
            path('clients/user/<int:id>/',views.CustomerByUser.as_view()),

            # commandes
            path('commandes/',views.CommandeAPIView.as_view()),
            path('commandes/<int:id>/',views.CommandeByIdAPIView.as_view()),
            path('commandes/user/<int:id>/',views.CommandeByUser.as_view()),

             # transaction
            path('transaction/',views.TransactionAPIView.as_view()),
            path('transaction/<int:id>/',views.TransactionByIdAPIView.as_view()),
            path('transaction/user/<int:id>/',views.TransactionByUser.as_view()),
            
            # commandes
            path('entree/',views.EntreeAPIView.as_view()),
            path('entree/<int:id>/',views.EntreeByIdAPIView.as_view()),
            path('entree/user/<int:id>/',views.EntreeByUser.as_view()),

            # profile 
            path('profiles/', views.ProfileList.as_view()),
            path('profiles/user/<int:id>/', views.ProfileByUser.as_view()),
            
            #parametre
            path('parametres/', views.ParametreList.as_view()),
            path('parametres/user/<int:id>/', views.ParametreByUser.as_view()),
            path('parametres/<int:id>/', views.ParametreByIdAPIView.as_view()),
            # path('profiles/<int:id>/', views.CompanyByIdAPIView.as_view()),

            # path('envoyer-message/', SendTwilioMessageView.as_view(), name='envoyer-message'),
            

            path('mail/', views.send_email),
            # path('mail/fac/', views.SendMailView.as_view()),
            
            

            # fournisseur 
            # path('fournisseur/', views.FournisseurAPIView.as_view()),
            # path('fournisseurs/', views.FournisseurAPIListView.as_view()),
            # path('fournisseur/upload',views.FournisseurUploadFileView.as_view()),
            # path('fournisseur/export',views.FournisseurExportFileView),
            # path('fournisseur/<int:id>', views.FournisseurByIdAPIView.as_view()),

            # category 
            # path('category/', views.CategoryAPIView.as_view()),
            # path('category/<int:id>/', views.CategoryByIdAPIView.as_view()),

            # product 
            # path('product/', views.ProductAPIView.as_view()),
            # path('product/<int:id>/', views.ProductByIdAPIView.as_view()),

            # vente 
            # path('vente/', views.VenteAPIView.as_view()),
            # path('vente/<int:id>/', views.VenteByIdAPIView.as_view()),
            # path('vente/mail/<int:id>/', views.SendVenteMailAPIView.as_view()),
            # path('statistic/<str:grouped_by>/', views.StatisticByDateAPIView.as_view({'get': 'list'})),


            # article 
            # path('article/', views.ArticleAPIListView.as_view()),
            # path('article/<int:id>/', views.ArticleByIdAPIView.as_view()),

            # depense 
            # path('depense/', views.DepenseAPIView.as_view()),
            # path('depense/<int:id>/', views.DepenseByIdAPIView.as_view()),

            # album 
            path('album/', views.AlbumAPIView.as_view()),
            path('album/<int:id>/', views.AlbumByIdAPIView.as_view()),
             path('album/user/<int:id>/',views.AlbumByUser.as_view()),

             # photos
            path('photo/', views.PhotoAPIView.as_view()),
            path('photo/<int:id>/', views.PhotoByIdAPIView.as_view()),
            path('photos/album/<int:id>/', views.getListPhotosByAlbumId.as_view()),

            # achat  
            # path('achat/', views.DepenseArticleAPIListView.as_view()),
            # path('achat/<int:id>/', views.DepenseArticleByIdAPIView.as_view()),

            # path('statistic',views.StatisticAPIListView.as_view()),

            #paiement
            # path('paiement/', CreationPaiementAPIView.as_view()),
            # path('paiement/<int:pk>/', ModifierPaiementAPIView.as_view()),
            # path('paiement/employee/<int:pk>/', getListPaimentByUser.as_view()),

            #employees
            # path('employees/', EmployeeList.as_view()),
            # path('emplyees/', CreateEmployee.as_view()),
            # path('employees/<int:pk>', DetailEmployee.as_view()),

        ])
    ),
]


if settings.DEBUG: 
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT) 