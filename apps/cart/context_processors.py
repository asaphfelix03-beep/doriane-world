from .models import Cart


def cart_summary(request):
    count = 0
    total = 0
    if request.session.session_key:
        cart = Cart.objects.filter(session_key=request.session.session_key).first()
        if cart:
            for item in cart.items.select_related("product"):
                count += item.quantity
                total += item.product.price * item.quantity
    return {"cart_item_count": count, "cart_total": total}
