from rest_framework.request import Request

from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from interview.order.models import Order, OrderTag
from interview.order.serializers import OrderSerializer, OrderTagSerializer

# Create your views here.
class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    

class OrderTagListCreateView(generics.ListCreateAPIView):
    queryset = OrderTag.objects.all()
    serializer_class = OrderTagSerializer


class DeactivateOrderView(APIView):
    serializer_class = OrderSerializer

    def post(self, request: Request, *args, **kwargs) -> Response:
        order_id = kwargs.get('id')
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found.'}, status=status.HTTP_404_NOT_FOUND)
        if not order.is_active:
            return Response({'error': 'The order is already deactivated.'}, status=status.HTTP_400_BAD_REQUEST)
        order.is_active = False
        order.save()

        serializer = self.serializer_class(order)
        return Response(serializer.data, status=status.HTTP_200_OK)
