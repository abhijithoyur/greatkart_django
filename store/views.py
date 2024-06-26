from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product
from category.models import Category
from carts.models import CartItem,Cart
from carts.views import _cart_id
# Create your views here.
def store(request,category_slug=None):
    category = None
    products = None
    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category = categories, is_available = True)
        paginator = Paginator(products, 3)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        product_count = products.count()
    else:
        products = Product.objects.all().filter(is_available = True).order_by('id')
        paginator = Paginator(products, 3)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        product_count = products.count()
    context = {
        'products' : page_obj,
        'product_count' : product_count
    }
    return render(request,'store/store.html', context)


def product_detail(request,category_slug,product_slug):
    try:
        product = get_object_or_404(Product,category__slug=category_slug, slug=product_slug, is_available=True)
        category = get_object_or_404(Category, slug=category_slug)
        in_cart = CartItem.objects.filter(cart__cart_id = _cart_id(request), product=product).exists()
    except Exception as e:
        raise e
    context ={
        'product' : product,
        'category' : category,
        'in_cart' : in_cart
    }
    return render(request,'store/product_detail.html', context)

def search(request):
    context={}
    if 'keyword' in request.GET :
        keyword = request.GET['keyword']
        if keyword :
            products = Product.objects.order_by('-created_date').filter(
                Q(description__icontains=keyword) | Q(product_name__icontains=keyword)
            )
        product_count = products.count()
        context = {
            'products' : products,
            'product_count' : product_count
        }
    return render(request,'store/store.html',context)
