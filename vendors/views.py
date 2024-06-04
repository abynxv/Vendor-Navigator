from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import logout, authenticate
from django.shortcuts import get_object_or_404

class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'Message': "User Created",'Token': token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'Message': "You are Logged In",'Token': token.key}, status=status.HTTP_200_OK)
        return Response({'Error': 'Wrong Credentials'}, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        token = Token.objects.get(user=request.user)
        token.delete()
        logout(request)
        return Response({'Message': 'User logged out successfully'}, status=status.HTTP_200_OK)
        

class VendorListView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        vendors = VendorModel.objects.all()
        serializer = VendorSerializer(vendors, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VendorDetailView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        vendor = get_object_or_404(VendorModel, pk=pk)
        serializer = VendorSerializer(vendor)
        return Response(serializer.data)

    def put(self, request, pk):
        vendor = get_object_or_404(VendorModel, pk=pk)
        serializer = VendorSerializer(vendor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        vendor = get_object_or_404(VendorModel, pk=pk)
        vendor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class PurchaseOrderListView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        vendor_id = request.query_params.get('vendor_id')
        if vendor_id:
            purchase_orders = PurchaseOrderModel.objects.filter(vendor_id=vendor_id)
        else:
            purchase_orders = PurchaseOrderModel.objects.all()
        serializer = PurchaseOrderSerializer(purchase_orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PurchaseOrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PurchaseOrderDetailsView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        purchase_order = get_object_or_404(PurchaseOrderModel, pk=pk)
        serializer = PurchaseOrderSerializer(purchase_order)
        return Response(serializer.data)

    def put(self, request, pk):
        purchase_order = get_object_or_404(PurchaseOrderModel, pk=pk)
        serializer = PurchaseOrderSerializer(purchase_order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        purchase_order = get_object_or_404(PurchaseOrderModel, pk=pk)
        purchase_order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class PurchaseOrderAcknowledgeView(APIView):
    def post(self, request, pk):
        purchase_order = get_object_or_404(PurchaseOrderModel, pk=pk)

        if purchase_order.acknowledgment_date is not None:
            return Response({'error': 'Purchase order already acknowledged.'}, status=status.HTTP_400_BAD_REQUEST)

        purchase_order.acknowledgment_date = date.today()
        delta = purchase_order.acknowledgment_date - purchase_order.order_date

        # Update the acknowledgment date in PurchaseOrderModel
        purchase_order.save()

        # Update the average response time in VendorModel
        vendor = purchase_order.vendor
        if vendor.average_response_time is not None:
            total_response_time = vendor.average_response_time * vendor.purchaseordermodel_set.count()
            new_average_response_time = (total_response_time + delta.days) / (vendor.purchaseordermodel_set.count() + 1)
        else:
            new_average_response_time = delta.days
        vendor.average_response_time = new_average_response_time
        vendor.save()

        serializer = PurchaseOrderSerializer(purchase_order)
        return Response({'Message':"Purchase Order Acknowledged"}, status=status.HTTP_200_OK)


class VendorPerformanceView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        vendor = get_object_or_404(VendorModel, pk=pk)
        performance_data = {
            'on_time_delivery_rate': vendor.on_time_delivery_rate,
            'quality_rating_avg': vendor.quality_rating_avg,
            'average_response_time': vendor.average_response_time,
            'fulfillment_rate': vendor.fulfillment_rate,
        }
        return Response(performance_data)
    
class HistoricalListView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk is None:
            historical_performances = HistoricalPerformanceModel.objects.all()
            serializer = HistoricalPerformanceSerializer(historical_performances, many=True)
            return Response(serializer.data)
        else:
            historical_performance = get_object_or_404(HistoricalPerformanceModel, pk=pk)
            serializer = HistoricalPerformanceSerializer(historical_performance)
            return Response(serializer.data)
        
class VendorHistoricalPerformanceView(APIView):
    def get(self, request, pk):
        vendor = get_object_or_404(VendorModel, pk=pk)
        historical_performances = vendor.historicalperformancemodel_set.all()
        serializer = HistoricalPerformanceSerializer(historical_performances, many=True)
        return Response(serializer.data)
    
