from decimal import Decimal

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType

import pytest
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import Client, TestCase, RequestFactory
from django.urls import reverse


from sushi.cart import Cart
from sushi.models import Product, Category, OrderItem


def test_index(db):
    client = Client()
    url = ''
    response = client.get(url)
    assert response.status_code == 200
    assert 'MySushi' in str(response.content)


def test_product_list(db, client):
    endpoint = reverse('sushi:product_list')
    response = client.get(endpoint)
    assert response.status_code == 200
    assert 'Wszystkie' in str(response.content)


def test_product_list_by_category(db, client, category):
    endpoint = reverse('sushi:product_list_by_category', args=(category.slug,))
    response = client.get(endpoint)
    assert response.status_code == 200


def test_product_detail(db, client, product):

    endpoint = reverse('sushi:product_detail', args=(product.id,))
    response = client.get(endpoint)
    assert response.status_code == 200


class CartInitializeTestCase(TestCase,):
    def test_cart_create(self):
        self.request = RequestFactory().get('sushi:cart_detail')
        request = self.request
        middleware = SessionMiddleware()
        middleware.process_request(self.request)
        self.request.session.save()


def test_cart(db, client, user):
    client.force_login(user)
    endpoint = reverse('sushi:cart_detail')
    response = client.get(endpoint)
    assert response.status_code == 200
    assert 'Do kasy' in str(response.content)



def test_order_create_get(db, client, user):
    client.force_login(user)
    endpoint = reverse('sushi:order_create')
    response = client.get(endpoint)
    assert response.status_code == 200
    assert 'Table number' in str(response.content)


@pytest.mark.django_db
def test_order_create_post(db, client, user):
    client.force_login(user)
    data = {'tabel number': '2'}
    endpoint = reverse('sushi:order_create')
    response = client.post(endpoint, data)
    products = OrderItem.objects.all()
    assert response.status_code == 200
    assert 'Order' in str(response.content)


@pytest.mark.django_db
def test_cart_add(db, client, user, product):
    client.force_login(user)
    endpoint = reverse('sushi:cart_add', args=(product.id,))
    response = client.post(endpoint)
    assert response.status_code == 302


@pytest.mark.django_db
def test_cart_remove(db, client, user, product):
    client.force_login(user)
    endpoint = reverse('sushi:cart_remove', args=(product.id,))
    response = client.post(endpoint)
    assert response.status_code == 302
    assert ''




class SignupPageTests(TestCase):
    def test_url_exists_at_correct_location_signupview(self):
        response = self.client.get("/accounts/signup/")
        self.assertEqual(response.status_code, 200)

    def test_signup_view_name(self):
        response = self.client.get(reverse('sushi:signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/signup.html")


@pytest.mark.django_db
def test_signup_post():
    client = Client()
    url = reverse('sushi:signup')
    data = {
        "Username": "Jaroslaw",
        "Email address": "wielki@gmail.com",
        "Age": '22',
        "Password": "alamakota1",
        "Password confirmation": "alamakota1",
    }
    response = client.post(url, data)
    assert response.status_code == 200


def test_delete_product(client, user):
    client.force_login(user)
    endpoint = reverse('sushi:cart_detail')


class CartAddTestCase(TestCase):
    def create(self):
        self.request = RequestFactory().get('/')

        middleware = SessionMiddleware()
        middleware.process_request(self.request)
        self.request.session['cart'] = {
            '1': {
                'name': 'some name',
                'price': '1.01',
                'quantity': 8,
            },
        }
        self.request.session.save()


def test_cart_add_to_existing_quantity(self):
    cart = Cart(self.request.session)
    cart.add(product=self.product,
                quantity=4,
                update_quantity=False,
                )
    new_cart = {
        '1': {
            'name': 'some name',
            'price': '1.01',
            'quantity': 12,
        },
    }
    self.assertEqual(cart.cart, new_cart)
