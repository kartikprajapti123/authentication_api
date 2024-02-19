from rest_framework import serializers
from .models import CustomUser,TokenForVerification,Order,OrderItem,Product
import re

from django.contrib.auth.hashers import make_password
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomUser
        
        fields=['id','first_name','last_name','email','password']
        extra_kwargs = {'password': {'write_only': True}}
        
    def validate(self, attrs):
        first_name=attrs.get('first_name')
        last_name=attrs.get('last_name')
        password=attrs.get('password')
        email=attrs.get('email')
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not first_name[0].isalpha():
           raise serializers.ValidationError("first name starts with aplhabet")
       
        elif not last_name[0].isalpha():
           raise serializers.ValidationError("Last name starts with aplhabet") 
       
        elif len(password) <8 or len(password) >14:
           raise serializers.ValidationError("password length should be between 8 to 14")
       
        elif not re.match(pattern,email):
            raise serializers.ValidationError("Invalid Email")
        
        return attrs
    
    def create(self, validated_data):
        # Hash the password before saving
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)
       
       
class ChangePasswordSerializer(serializers.ModelSerializer):
    password2=serializers.CharField(write_only=True)
    
    class Meta:
        model=CustomUser
        
        fields=['password','password2']
        
    def validate(self, attrs):
        password=attrs.get('password')
        password2=attrs.get('password2')
        token=self.context.get('token')
        
        PrevTokenUser=TokenForVerification.objects.filter(token=token)
        if PrevTokenUser.exists():
            user=PrevTokenUser[0].user
            if len(password)<8 or len(password) >14:
                raise serializers.ValidationError("password length should be 8 to 14")
            elif password!=password2:
                raise serializers.ValidationError("password one is not macthing")
            
            user.set_password(password)
            user.save()
            
        else:
            raise serializers.ValidationError("token is invalid")
        

        return attrs
 