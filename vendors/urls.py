from .views import *
from django.urls import path

urlpatterns = [

    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('vendors/',VendorListView.as_view()),
    path('vendors/<int:pk>/',VendorDetailView.as_view()),
    path('vendors/<int:pk>/performance/',VendorPerformanceView.as_view()),
    path('vendors/historical_performance/',HistoricalListView.as_view()),
    path('vendors/<int:pk>/historical_performance/',VendorHistoricalPerformanceView.as_view()),

    path('purchase_orders/',PurchaseOrderListView.as_view()),
    path('purchase_orders/<int:pk>/',PurchaseOrderDetailsView.as_view()),
    path('purchase_orders/<int:pk>/acknowledge/',PurchaseOrderAcknowledgeView.as_view()),

]
