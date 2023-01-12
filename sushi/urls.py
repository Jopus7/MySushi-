from django.urls import path
from . import views
from .views import SignUpView
from sushi import views

app_name = 'sushi'
urlpatterns = [


    path('', views.product_list, name='product_list'),
    path('category/<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('<int:id>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:product_id>', views.cart_remove, name='cart_remove'),
    path('orders/create/', views.order_create, name='order_create'),
    path('signup/', SignUpView.as_view(), name='signup'),
]
