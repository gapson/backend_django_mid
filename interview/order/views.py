from pydantic.datetime_parse import parse_date
from rest_framework.request import Request
from django.http import Http404

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

    @staticmethod
    def parse_str_date(date_str: 'Date'):
        try:
            date = parse_date(date_str)
        except Exception:  # could catch the pydantic.errors.DateError only
            return None
        return date

    def get(self, request: Request, *args, **kwargs) -> Response:
        orders = self.get_queryset()
        date_start_str = request.query_params.get('date-start', None)
        date_end_str = request.query_params.get('date-end', None)
        error_msg = {'error': 'Invalid date format. Use YYYY-MM-DD.'}
        if date_start_str:
            start = self.parse_str_date(date_start_str)
            if not start:
                return Response(error_msg, status=status.HTTP_400_BAD_REQUEST)
            orders = orders.filter(created_at__gt=start)
        if date_end_str:
            end_date = self.parse_str_date(date_end_str)
            if not end_date:
                return Response(error_msg, status=status.HTTP_400_BAD_REQUEST)
            orders = orders.filter(created_at__lt=end_date)

        serializer = self.serializer_class(orders, many=True)
        return Response(serializer.data, status=200)
    

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
