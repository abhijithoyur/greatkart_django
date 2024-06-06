from carts.models import Cart, CartItem
from carts.views import _cart_id

def counter(request):
    if 'admin' in request.path:
        return {}
    else:
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))  # Use get to retrieve a single Cart object
            cart_items = CartItem.objects.filter(cart=cart)  # Filter CartItem instances by the retrieved Cart object
            cart_count = cart_items.count()  # Count the number of unique CartItem instances
        except Cart.DoesNotExist:
            cart_count = 0
    return dict(cart_count=cart_count)
