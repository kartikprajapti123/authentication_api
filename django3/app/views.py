from django.contrib.auth import authenticate, login,logout
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from django.views.decorators.csrf import csrf_exempt
from .models import CustomUser,TokenForVerification,Order,OrderItem,Product
from rest_framework.decorators import action
from app.serializers import CustomUserSerializer,ChangePasswordSerializer# Assuming you have a serializer file

from rest_framework_simplejwt.authentication import JWTAuthentication

from rest_framework.permissions import IsAuthenticatedOrReadOnly,IsAuthenticated
from rest_framework.authentication import BasicAuthentication
import uuid
from django3 import settings

from django.core.mail import send_mail


from rest_framework_simplejwt.tokens import RefreshToken

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class CustomUserView(ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    @action(detail=False,methods=['post'],permission_classes=[AllowAny])
    def login(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        print(email,password)
        user = authenticate(request, email=email, password=password)
        print(user)
        if user is not None:
            token=get_tokens_for_user(user)
            login(request, user)
            return Response({'token':token,'msg': 'Successfully login'})
        else:
            return Response({'error': 'Email or password is invalid'})
        
    @action(detail=False,methods=['post'],permission_classes=[AllowAny])    
    def signup(self,request,*args,**kwargs):
        serializer=CustomUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'msg':'Successfully singup'})
    
    
    @csrf_exempt
    @action(detail=False,methods=['POST'],permission_classes = [IsAuthenticated],
    authentication_classes = [JWTAuthentication])
    def logout(self,request):
        print(request.user)
        logout(request)
        
        return Response({'msg':'Successfully'})
    
    
    @action(detail=False,methods=['post'],permission_classes=[AllowAny])
    def sendmail(self,request):
        email=request.data.get('email')
        user=CustomUser.objects.filter(email=email)
        
        if user.exists():
            token=str(uuid.uuid4())
            TokenForVerification.objects.create(token=token,user=user[0])
            subject = 'welcome to GFG world'
            message = f'Hi {user[0].first_name}, thank you for registering in xyz website\n this is email for your verification http://127.0.01:8000/user/{token}/.'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [f'{email}']
            send_mail( subject, message, email_from, recipient_list )
            return Response({"msg":'email is send'})
        else:
            return Response({"msg":'You are not logged before first login'})
            
                    
                    
    @action(detail=False,methods=['post','get'],permission_classes=[AllowAny])
    def ChangePassword(self,request,**kwargs):
        token=kwargs.get('token',None)
        print(token)
        if request.method=="GET":
            print(token)
            UserToken=TokenForVerification.objects.filter(token=token)
            if UserToken.exists():
                return Response({'msg':"Token is valid"})
            
            else:
                return Response({'error':"token is not valid"})
        
        if request.method=="POST":
            print("post")
            serializer=ChangePasswordSerializer(data=request.data,context={'token':token})
        
            serializer.is_valid(raise_exception=True)
            
            return Response({'msg':"Password has been changed"})
        
 