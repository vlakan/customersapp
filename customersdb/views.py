from django.http import HttpResponse
from django.urls import reverse_lazy
from django.db.models import Q
from django.views import View
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, DeleteView
from .models import Customer
from .forms import CustomerForm
from openpyxl import Workbook


class CustomersListView(ListView):
    model = Customer
    template_name = 'customersdb/customers_list.html'
    context_object_name = 'customers'
    ordering = 'pk'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        sort_by = self.request.GET.get('sort_by')

        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) | Q(surname__icontains=query)
            )

        if sort_by:
            queryset = queryset.order_by(sort_by)

        return queryset


class CustomerCreateView(CreateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'customersdb/customer_add.html'
    success_url = reverse_lazy('customers_list')


class CustomerDetailView(DetailView):
    model = Customer
    template_name = 'customersdb/customer_detail.html'
    context_object_name = 'customer'


class CustomerDeleteView(DeleteView):
    model = Customer
    template_name = 'customersdb/customer_confirm_delete.html'
    success_url = reverse_lazy('customers_list')


class ExportCustomersView(View):
    def get(self, request):
        customers = Customer.objects.all()
        workbook = Workbook()
        worksheet = workbook.active

        worksheet.append(['First Name', 'Last Name', 'Age', 'Date of Birth'])

        for customer in customers:
            worksheet.append([customer.name, customer.surname, customer.age, customer.date_birth])

        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=customer_cards.xlsx'
        workbook.save(response)

        return response
