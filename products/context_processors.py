from .models import Cart


def cart_item_count(request):
    cart = Cart.objects.filter(session_key=request.session.session_key).first()

    if cart:
        count = sum(item.quantity for item in cart.items.all())
    else:
        count = 0

    return {
        'cart_item_count': count
    }
