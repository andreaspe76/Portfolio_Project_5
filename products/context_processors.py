from .models import Cart


def cart_item_count(request):
    cart_id = request.session.get('cart_id')

    if not cart_id:
        return {'cart_item_count': 0}

    try:
        cart = Cart.objects.get(id=cart_id)
        count = sum(item.quantity for item in cart.items.all())
    except Cart.DoesNotExist:
        count = 0

    return {'cart_item_count': count}
