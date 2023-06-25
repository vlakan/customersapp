from django.test import TestCase
from django.urls import reverse
from .models import Customer


class CustomerListViewTest(TestCase):
    def test_customer_list_view(self):
        response = self.client.get(reverse('customers_list'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Customers List')
        self.assertTemplateUsed(response, 'customersdb/customers_list.html')


class CustomerDetailViewTest(TestCase):
    def test_customer_detail_view(self):
        customer = Customer.objects.create(name='John', surname='Doe', age=30, date_birth='1993-01-01',
                                           photo='media/images/photo_2023-05-30_20-08-47.jpg')

        response = self.client.get(reverse('customer_detail', kwargs={'pk': customer.pk}))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'John Doe')
        self.assertTemplateUsed(response, 'customersdb/customer_detail.html')


class CustomerAddViewTest(TestCase):
    def test_customer_add_view(self):
        response = self.client.get(reverse('customer_add'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'customersdb/customer_add.html')

        # Test adding a new customer
        form_data = {
            'name': 'Jane',
            'surname': 'Smith',
            'age': 25,
            'date_birth': '1998-05-10',
            'photo': 'media/images/photo_2023-05-30_20-08-47.jpg',
        }
        response = self.client.post(reverse('customer_add'), data=form_data)
        self.assertEqual(response.status_code, 302)

        redirect_url = response['Location']
        redirected_response = self.client.get(redirect_url)

        self.assertEqual(redirected_response.status_code, 200)
        self.assertContains(redirected_response, 'Smith')
        self.assertTemplateUsed(redirected_response, 'customersdb/customers_list.html')


class CustomerDeleteViewTest(TestCase):
    def test_customer_delete_view(self):
        photo = 'images/photo_2023-06-20_20-40-34.jpg'
        customer = Customer.objects.create(name='John', surname='Doe', age=30, date_birth='1993-01-01',
                                           photo=photo)

        response = self.client.get(reverse('customer_delete', kwargs={'pk': customer.pk}))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Are you sure you want to delete John Doe')
        self.assertTemplateUsed(response, 'customersdb/customer_confirm_delete.html')

        # Test deleting a customer
        response = self.client.post(reverse('customer_delete', kwargs={'pk': customer.pk}), follow=True)

        self.assertEqual(response.status_code, 200)  # Check for successful deletion
        self.assertNotContains(response, 'Doe')
        self.assertTemplateUsed(response, 'customersdb/customers_list.html')


class ExportCustomersViewTest(TestCase):
    def test_export_customers_view(self):
        response = self.client.get(reverse('export_customers'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get('Content-Type'),
                         'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        self.assertEqual(response.get('Content-Disposition'), 'attachment; filename=customer_cards.xlsx')
