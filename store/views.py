from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Product, CartItem, ProductForm
from django.db.models import F, Sum

def product_list(request):
    products = Product.objects.all()
    return render(request, 'store/product_list.html', {'products': products})

def cart(request):
    cart_items = CartItem.objects.all()
    return render(request, 'store/cart.html', {'cart_items': cart_items})

def add_to_cart(request, product_id):
    if request.method == "POST":
        product = get_object_or_404(Product, id=product_id)
        cart_item, created = CartItem.objects.get_or_create(product=product)
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        return redirect('cart')  # Перенаправляем пользователя на страницу корзины
    return HttpResponse("Invalid request", status=400)

def clear_cart(request):
    # Удаляем все элементы из корзины
    CartItem.objects.all().delete()
    # Перенаправляем обратно на страницу корзины
    return redirect('cart')

def cart(request):
    cart_items = CartItem.objects.all()
    total_price = cart_items.aggregate(total=Sum(F('quantity') * F('product__price')))['total'] or 0
    return render(request, 'store/cart.html', {'cart_items': cart_items, 'total_price': total_price})

@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'store/add_product.html', {'form': form})