from django.contrib import admin
from django.conf import settings 
from django.urls import path, include

from drf_yasg import openapi
from drf_yasg.views import get_schema_view as swagger_get_schema_view
from . import views
from django.conf.urls.static import static 

schema_view = swagger_get_schema_view(
    openapi.Info(
        title="Fewnu Compta",
        default_version='1.0.0',
        description="API documentation of Fewnu Gestion Compta",
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
            path('user/<int:id>', views.UserById.as_view()),
            path('user/password/<int:id>', views.UserUpdatePassword.as_view()),
            path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name="swagger-schema"),

            # clients 
            path('clients',views.CustomerAPIListView.as_view()),
            path('client',views.CustomerAPIView.as_view()),
            path('client/upload',views.CustomerUploadFileView.as_view()),
            path('client/export',views.CustomerExportFileView),
            path('client/<int:id>/',views.CustomerByIdAPIView.as_view()),

            # company 
            path('company/', views.CompanyAPIView.as_view()),
            path('company/<int:id>/', views.CompanyByIdAPIView.as_view()),
            

            path('mail/', views.send_email),
            # path('mail/fac/', views.SendMailView.as_view()),
            
            

            # fournisseur 
            path('fournisseur/', views.FournisseurAPIView.as_view()),
            path('fournisseurs/', views.FournisseurAPIListView.as_view()),
            path('fournisseur/upload',views.FournisseurUploadFileView.as_view()),
            path('fournisseur/export',views.FournisseurExportFileView),
            path('fournisseur/<int:id>', views.FournisseurByIdAPIView.as_view()),

            # category 
            path('category/', views.CategoryAPIView.as_view()),
            path('category/<int:id>/', views.CategoryByIdAPIView.as_view()),

            # product 
            path('product/', views.ProductAPIView.as_view()),
            path('product/<int:id>/', views.ProductByIdAPIView.as_view()),

            # vente 
            path('vente/', views.VenteAPIView.as_view()),
            path('vente/<int:id>/', views.VenteByIdAPIView.as_view()),
            path('vente/mail/<int:id>/', views.SendVenteMailAPIView.as_view()),
            # path('statistic/<str:grouped_by>/', views.StatisticByDateAPIView.as_view({'get': 'list'})),


            # article 
            path('article/', views.ArticleAPIListView.as_view()),
            path('article/<int:id>/', views.ArticleByIdAPIView.as_view()),

            # depense 
            path('depense/', views.DepenseAPIView.as_view()),
            path('depense/<int:id>/', views.DepenseByIdAPIView.as_view()),

            # achat  
            path('achat/', views.DepenseArticleAPIListView.as_view()),
            path('achat/<int:id>/', views.DepenseArticleByIdAPIView.as_view()),

            path('statistic',views.StatisticAPIListView.as_view()),

            #paiement
            path("creation_paiement/", views.Creation_paiementAPIView.as_view()),
        ])
    ),
]


if settings.DEBUG: 
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT) 