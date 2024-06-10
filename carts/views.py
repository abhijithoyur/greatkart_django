from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404
from carts.models import Cart,CartItem
from store.models import Product


# Create your views here.

#cart id is a private function, that's why it is starting with underscore
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    print(product)
    try :
        cart = Cart.objects.get(cart_id = _cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id =_cart_id(request)
        )
        cart.save()
    try:
        cart_item = CartItem.objects.get(product=product,cart=cart)
        # if product.stock > cart_item.cart_quantity:
        cart_item.cart_quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product = product,
            cart_quantity = 1,
            cart = cart
        )
        cart_item.save()
    return redirect('cart')

def dec_to_cart(request, product_id):
    cart = Cart.objects.get(cart_id = _cart_id(request))
    product = get_object_or_404(Product,id=product_id)
    cart_item = CartItem.objects.get(product=product,cart=cart)
    if cart_item.cart_quantity > 1:
        cart_item.cart_quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')

def remove_from_cart(request,product_id):
    cart = Cart.objects.get(cart_id = _cart_id(request))
    product = get_object_or_404(Product,id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    cart_item.delete()
    return redirect('cart')

def cart(request, total=0, cart_quantity=0, cart_items=None):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items =CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += round(cart_item.product.price * cart_item.cart_quantity,2)
            cart_quantity += cart_item.cart_quantity
        tax = round(total * 0.18,2)
        grand_total = round(total + tax,2)
    except ObjectDoesNotExist:
        pass
    context = {
        'total' : total,
        'cart_quantity' : cart_quantity,
        'cart_items': cart_items,
        'tax' : tax,
        'grand_total' : grand_total
    }
    return render(request,'store/cart.html',context)
