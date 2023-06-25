from django.urls import path
from .views import CustomersListView, CustomerCreateView, CustomerDetailView, CustomerDeleteView, ExportCustomersView

urlpatterns = [
    path('', CustomersListView.as_view(), name='customers_list'),
    path('customer/add/', CustomerCreateView.as_view(), name='customer_add'),
    path('customer/<int:pk>/', CustomerDetailView.as_view(), name='customer_detail'),
    path('customer/<int:pk>/delete/', CustomerDeleteView.as_view(), name='customer_delete'),
    path('export/', ExportCustomersView.as_view(), name='export_customers'),
]
