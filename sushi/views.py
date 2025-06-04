from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.generic import CreateView
from .forms import CustomUserCreationForm, CartAddProductForm, OrderCreateForm, AddressForm
from .models import Product, Category, Cart, CartItem, OrderItem, Order


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
    product = get_object_or_404(Product, id=id, available=True)
    cart_product_form = CartAddProductForm()
    return render(request, 'product_detail.html', {
        'product': product,
        'cart_product_form': cart_product_form,
    })


@require_POST
@login_required
def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get("quantity", 1))
    override = request.POST.get("override", "false") == "true"

    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if override:
        if quantity == 0:
            cart_item.delete()
        else:
            cart_item.quantity = quantity
            cart_item.save()
    else:
        cart_item.quantity += quantity
        cart_item.save()
    return redirect('sushi:cart_detail')


@require_POST
@login_required
def cart_remove(request, product_id):
    cart = get_object_or_404(Cart, user=request.user)
    try:
        cart_item = CartItem.objects.get(cart=cart, product_id=product_id)
        cart_item.delete()
    except CartItem.DoesNotExist:
        pass
    return redirect('sushi:cart_detail')


@login_required
def cart_detail(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    items = cart.items.select_related('product')

    if request.method == 'POST':
        for item in items:
            quantity = request.POST.get(f'quantity_{item.id}')
            if quantity:
                item.quantity = int(quantity)
                item.save()
        return redirect('sushi:cart_detail')

    return render(request, 'cart_detail.html', {'cart': cart, 'items': items, 'total_cost': cart.get_total_cost()})


@login_required
def order_create(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        form.fields['delivery_address'].queryset = request.user.addresses.all()
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()

            for item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )
            cart.items.all().delete()
            return redirect('sushi:order_success')
    else:
        form = OrderCreateForm()
        form.fields['delivery_address'].queryset = request.user.addresses.all()

    return render(request, 'order_create.html', {
        'form': form,
        'items': cart.items.all(),  # ← TO MUSI BYĆ
        'total_cost': cart.get_total_cost()  # ← i to
    })


@login_required
def order_success(request):
    return render(request, 'order_success.html')

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


@login_required
def add_address(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            return redirect('sushi:product_list')
    else:
        form = AddressForm()
    return render(request, 'address_form.html', {'form': form})
