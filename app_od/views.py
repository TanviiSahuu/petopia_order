from rest_framework import viewsets, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Order, OrderDetails, Payment
from .serializer import OrderSerializer, OrderDetailsSerializer, PaymentSerializer
import uuid
from django.utils.timezone import now

# CRUD Operations for Orders
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def list(self, request):
        """Fetch all orders"""
        orders = Order.objects.all()
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Fetch order by ID"""
        order = get_object_or_404(Order, order_id=pk)
        serializer = self.get_serializer(order)
        return Response(serializer.data)

    def create(self, request):
        """Create a new order"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(order_id=uuid.uuid4())  # Generate UUID
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        """Update order by ID"""
        order = get_object_or_404(Order, order_id=pk)
        serializer = self.get_serializer(order, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """Delete order by ID"""
        order = get_object_or_404(Order, order_id=pk)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# CRUD Operations for Order Details
class OrderDetailsViewSet(viewsets.ModelViewSet):
    queryset = OrderDetails.objects.all()
    serializer_class = OrderDetailsSerializer

    def list(self, request):
        """Fetch all order details"""
        order_details = OrderDetails.objects.all()
        serializer = self.get_serializer(order_details, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Fetch order details by ID"""
        order_detail = get_object_or_404(OrderDetails, order_details_id=pk)
        serializer = self.get_serializer(order_detail)
        return Response(serializer.data)

    def create(self, request):
        """Create new order details"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(order_details_id=uuid.uuid4())  # Generate UUID
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        """Update order details by ID"""
        order_detail = get_object_or_404(OrderDetails, order_details_id=pk)
        serializer = self.get_serializer(order_detail, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """Delete order details by ID"""
        order_detail = get_object_or_404(OrderDetails, order_details_id=pk)
        order_detail.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# CRUD Operations for Payments (with validation)
class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def list(self, request):
        """Fetch all payments"""
        payments = Payment.objects.all()
        serializer = self.get_serializer(payments, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Fetch payment by ID"""
        payment = get_object_or_404(Payment, payment_id=pk)
        serializer = self.get_serializer(payment)
        return Response(serializer.data)

    def create(self, request):
        """Create payment with validation"""
        data = request.data
        order_id = data.get("order_id")
        amount = data.get("amount")
        method = data.get("method")
        payment_status = data.get("status")

        if not order_id:
            return Response({"error": "Order ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            order = Order.objects.get(order_id=order_id)
        except Order.DoesNotExist:
            return Response({"error": "Invalid Order ID"}, status=status.HTTP_404_NOT_FOUND)

        if order.total_amount != float(amount):
            return Response({"error": "Payment amount does not match order total"}, status=status.HTTP_400_BAD_REQUEST)

        payment = Payment.objects.create(
            payment_id=uuid.uuid4(),
            order=order,
            amount=amount,
            payment_date=now(),
            method=method,
            status=payment_status  
        )

        if payment_status.lower() == "successful":
            order.payment_status = "Paid"
            order.save()

        return Response(PaymentSerializer(payment).data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        """Update payment by ID"""
        payment = get_object_or_404(Payment, payment_id=pk)
        serializer = self.get_serializer(payment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """Delete payment by ID"""
        payment = get_object_or_404(Payment, payment_id=pk)
        payment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
