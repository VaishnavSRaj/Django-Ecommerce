from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from Ecommerce_app.models import Product
from cart.models import Cart, cart_item
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.


def _cart_id(request):
    cart_id = request.session.session_key
    if not cart_id:
        cart_id = request.session.create()
    return cart_id


def add_cart(request, product_id):
    cart = None
    Cart_item = None

    product = Product.objects.get(id=product_id)
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id=_cart_id(request)
        )
        cart.save()

    try:
        Cart_item = cart_item.objects.get(product=product, cart=cart)
        if Cart_item.quantity < int(Cart_item.product.stock):
          Cart_item.quantity += 1  # Cart_items.quantity = Cart_items.quantity +1
        Cart_item.save()


    except cart_item.DoesNotExist:

        Cart_item = cart_item.objects.create(product=product, quantity=1, cart=cart)

        Cart_item.save()
        print('quantity=', Cart_item.quantity)

    return redirect('cart:cart')


def remove_cart(request, product_id):
    print('remove cart')
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    print(cart)
    cart_items = cart_item.objects.get(cart=cart, product=product)
    if cart_items.quantity > 1:
        cart_items.quantity -= 1
        cart_items.save()
        print('quantity -1', cart_item.quantity)
    else:
        cart_items.delete()
        cart_items.save()
        print('quantity -1', cart_item.quantity)
    return redirect('cart:cart')

def delete_cart_item(request , product_id):
    cart=Cart.objects.get(cart_id=_cart_id(request))
    product= get_object_or_404(Product, id=product_id)
    cart_items = cart_item.objects.get(cart=cart, product=product)
    cart_items.delete()
    return redirect('cart:cart')



def cart(request, total=0, quantity=0, Cart_item=None):

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        Cart_item = cart_item.objects.filter(cart=cart, active=True)
        for cart_items in Cart_item:
            total += (cart_items.product.price * cart_items.quantity)
            quantity += cart_items.quantity




    except ObjectDoesNotExist:
        pass

    return render(request, 'cart.html', dict(total=total, quantity=quantity, Cart_item=Cart_item))
