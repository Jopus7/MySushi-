import pytest

from sushi.models import Product, Category, Cart, Order, OrderItem


@pytest.fixture()
def user(db, django_user_model):

    user = django_user_model.objects.create_user(username='Test', email='test@test.pl', age=22,
                                                 password='Testpass123')
    return user

@pytest.fixture()
def category():
    return Category.objects.create(name='Futomaki')


@pytest.fixture()
def product(category):
    return Product.objects.create(category=category,
                                  name='Ginger',
                                  slug='ginger',
                                  description='ginger',
                                  price=5.00,
                                  available=True)

@pytest.fixture()
def cart(user):
    return Cart.objects.create(user=user, created_at='Dec. 16, 2022, 12:01 a.m.')


@pytest.fixture()
def order(user, product):
    return Order.objects.create(user=user,
                                table_number='2',
                                product=product,
                                delivered=False,
                                paid=False,
                                created='Dec. 16, 2022, 12:02 a.m.')

@pytest.fixture()
def order_item(order, product):
    return OrderItem.objects.create(order=order,
                                    product=product,
                                    quantity=2,
                                    price='5,00')
