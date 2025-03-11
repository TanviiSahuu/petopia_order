from django.contrib import admin
from app_od.models import Order
from app_od.models import OrderDetails
from app_od.models import Payment
admin.site.register(Order)
admin.site.register(OrderDetails)
admin.site.register(Payment)
# Register your models here.
