from .models import cart_item ,Cart
from .views import _cart_id


def counter(request):
    cart_count=0
    if 'admin' in request.path:
        return {}
    else:
        try:
            cart=Cart.objects.filter(cart_id=_cart_id(request))
            cart_items=cart_item.objects.all().filter(cart=cart[:1])
            for cartItem in cart_items:
                cart_count += cartItem.quantity
        except cart.DoesNotExist:
            cart_count=0
    return dict(cart_count=cart_count)

