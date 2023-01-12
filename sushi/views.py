
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import View
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, TemplateView, DetailView, ListView, UpdateView, DeleteView
from .forms import CustomUserCreationForm, CartAddProductForm, OrderCreateForm
from .models import Product, Category, Cart, OrderItem
from .cart import Cart


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request, 'product-list.html', {
        'category': category,
        'categories': categories,
        'products': products,
    })


def product_detail(request, id):
    product = get_object_or_404(Product, id=id,  available=True)
    cart_product_form = CartAddProductForm()
    return render(request, 'product_detail.html', {
        'product': product,
        'cart_product_form': cart_product_form,
    })


@require_POST
def cart_add(request, product_id):
    if request.user.is_authenticated:

        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        form = CartAddProductForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            cart.add(product=product,
                     quantity=cd['quantity'],
                     override_quantity=cd['override'])
        return redirect('sushi:cart_detail')
    else:
        return HttpResponse("Log in to continue")


@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('sushi:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'], 'override': True})
    return render(request, 'cart_detail.html', {'cart': cart})


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order,

                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'],

                                         )
                cart.clear()

            return render(request, 'order_created.html', {
                                'order': order,
                            })
    else:
        form = OrderCreateForm()
    return render(request, 'order_create.html', {
                        'cart': cart,
                        'form': form,
                    })


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'





























