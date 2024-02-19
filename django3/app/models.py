# users/models.py
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email
    
    
    class Meta:
        permissions=[
            ('cancel_order','can cancel order')
        ]
        
        
class TokenForVerification(models.Model):
    token=models.CharField(max_length=100)
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="reverseuser")
    
    def __str__(self):
        return self.user.email
    
class Product(models.Model):
    name=models.CharField(max_length=20)
    title=models.CharField(max_length=100)
    price=models.IntegerField()
    
    def __str__(self):
        return self.name    
    

class Order(models.Model):
    placed_at=models.DateTimeField(auto_now_add=True)
    payment_status=models.CharField(max_length=100)
    customer=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="ordercustomer")
    
class OrderItem(models.Model):
    order=models.ForeignKey(Order,on_delete=models.PROTECT,related_name="items")
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name="productitems")
    quantity=models.IntegerField()
    

