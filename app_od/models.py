from django.db import models
import uuid
from django.utils.timezone import now

# Order Model
class Order(models.Model):
    order_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer_id = models.UUIDField()
    order_date_time = models.DateTimeField(default=now)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

# Order Details Model
class OrderDetails(models.Model):
    order_details_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product_id = models.UUIDField()
    quantity = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

# Payment Model
class Payment(models.Model):
    payment_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(default=now)
    method = models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=[('Completed', 'Completed'), ('Failed', 'Failed')])