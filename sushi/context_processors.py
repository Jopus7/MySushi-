from .models import Cart

def cart_context(request):
    cart_items_count = 0
    cart_total_cost = 0

    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items_count = cart.items.count()
        cart_total_cost = cart.get_total_cost()

    return {
        'cart_items_count': cart_items_count,
        'cart_total_cost': cart_total_cost,
    }
