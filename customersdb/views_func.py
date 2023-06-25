from django.shortcuts import render, redirect, reverse
from django.http import HttpRequest, HttpResponse
from .models import Customer
from .forms import CustomerForm
from openpyxl import Workbook
from django.db.models import Q


def customers_list(request: HttpRequest) -> HttpResponse:
    query = request.GET.get('q')
    sort_by = request.GET.get('sort_by')

    if query:
        customers = Customer.objects.filter(
            Q(name__icontains=query) | Q(surname__icontains=query)
        )
    else:
        customers = Customer.objects.all()

    if sort_by:
        customers = customers.order_by(sort_by)

    return render(request, 'customersdb/customers_list.html', {'customers': customers})


def customer_add(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            url = reverse('customers_list')
            return redirect(url)
    else:
        form = CustomerForm()
    return render(request, 'customersdb/customer_add.html', {'form': form})


def customer_detail(request: HttpRequest, pk: int) -> HttpResponse:
    customer = Customer.objects.get(pk=pk)
    return render(request, 'customersdb/customer_detail.html', {'customer': customer})


def customer_delete(request: HttpRequest, pk: int) -> HttpResponse:
    customer = Customer.objects.get(pk=pk)
    if request.method == 'POST':
        customer.delete()
        url = reverse('customers_list')
        return redirect(url)
    return render(request, 'customersdb/customer_confirm_delete.html', {'customer': customer})


def export_customers(request: HttpRequest) -> HttpResponse:
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
