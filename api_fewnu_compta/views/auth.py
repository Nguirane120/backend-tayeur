from rest_framework import generics, permissions, status
from api_fewnu_compta.serializers import *
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authentication import TokenAuthentication, SessionAuthentication, BasicAuthentication
from django.contrib.auth import authenticate, login
from rest_framework_jwt.settings import api_settings
from rest_framework.response import Response
from django.contrib.auth import logout
from django.http import HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from api_fewnu_compta.models import User 


jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER



class LoginView(generics.CreateAPIView):
    """
    POST api/v1/login/
    """
    queryset = User.objects.all()
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        # email = request.data["email"]
        phone = request.data["phone"]
        password = request.data["password"]
        
        if not password:
            return Response(data={"message": "Both identifiant and password are required to connect"},status=400)
        else:
            try:
                if phone :
                    # userData = User.objects.get(phone=phone)
                    # print("user data in phone", userData)
                    user = authenticate(request, phone=phone, password=password)
                # elif email :
                #     user = authenticate(request, email=email, password=password)
                #     print("user data in email")
                # print("user",user)
                if user is not None:
                    login(request, user)
                    # Redirect to a success page.
                    serializer = TokenSerializer(data={"token": jwt_encode_handler(jwt_payload_handler(user))})
                    if serializer.is_valid():
                        token = serializer.data
                        response_data = {
                            'id': user.id,
                            'token': token,
                            'phone': user.phone,
                            'firstName': user.firstName,
                            'lastName': user.lastName,
                            'phone': user.phone,
                            # 'email':user.email,
                            'user_type':user.user_type,
                        }
                        return Response(response_data)   
                else:
                    return Response(data={"message": "Votre numero de telephone ou mot de passe est incorrect"},status=401)
            except User.DoesNotExist:
                return Response(data={"message": "Ce numero de telephone n'existe pas"},status=401)
@method_decorator(ensure_csrf_cookie, name='dispatch')
class GetCSRFToken(APIView):
    def get(self, request, format=None):
        print(request.META['CSRF_COOKIE'])
        return Response({ 'success': 'CSRF cookie set',"csrftoken":request.META['CSRF_COOKIE'] })
        
def logout_view(request):
    logout(request)



