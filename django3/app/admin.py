from django.contrib import admin
from .models  import CustomUser
from .models  import TokenForVerification,Order,OrderItem,Product
# Register your models here.
admin.site.register(CustomUser)
admin.site.register(TokenForVerification)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Product)





