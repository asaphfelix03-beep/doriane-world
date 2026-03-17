from urllib.parse import quote
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from apps.products.models import Product
from .models import Cart, CartItem
from .services import get_or_create_cart


def cart_detail(request):
    items = []
    total = 0
    cart = None
    if request.session.session_key:
        cart = Cart.objects.filter(session_key=request.session.session_key).first()
        if cart:
            items = cart.items.select_related("product")
            total = sum(item.product.price * item.quantity for item in items)
    return render(request, "cart/cart_detail.html", {"cart": cart, "items": items, "total": total})


@require_POST
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if product.stock == 0:
        return redirect("product_detail", slug=product.slug)

    try:
        quantity = int(request.POST.get("quantity", 1))
    except ValueError:
        quantity = 1

    quantity = max(1, quantity)
    if product.stock and quantity > product.stock:
        quantity = product.stock

    cart = get_or_create_cart(request)
    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if created:
        item.quantity = quantity
    else:
        new_qty = item.quantity + quantity
        if product.stock and new_qty > product.stock:
            new_qty = product.stock
        item.quantity = new_qty
    item.save()
    return redirect("cart_detail")


@require_POST
def update_cart(request):
    item_id = request.POST.get("item_id")
    item = get_object_or_404(CartItem, id=item_id)
    try:
        quantity = int(request.POST.get("quantity", 1))
    except ValueError:
        quantity = 1

    if quantity <= 0:
        item.delete()
    else:
        if item.product.stock and quantity > item.product.stock:
            quantity = item.product.stock
        item.quantity = quantity
        item.save()
    return redirect("cart_detail")


@require_POST
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    item.delete()
    return redirect("cart_detail")


def quick_order_whatsapp(request):
    cart = get_or_create_cart(request)
    items = cart.items.select_related("product")
    if not items.exists():
        return redirect("shop")
    lines = [f"{item.product.name} x {item.quantity}" for item in items]
    message = "Commande rapide Doriane World:\n" + "\n".join(lines)
    url = f"https://wa.me/{settings.WHATSAPP_NUMBER}?text={quote(message)}"
    return redirect(url)


def quick_order_email(request):
    cart = get_or_create_cart(request)
    items = cart.items.select_related("product")
    if not items.exists():
        return redirect("shop")
    sent_items = [{"name": item.product.name, "qty": item.quantity} for item in items]
    lines = ["Commande rapide Doriane World:", ""]
    for item in sent_items:
        lines.append(f"- {item['name']} x {item['qty']}")
    send_mail(
        "Commande rapide - Doriane World",
        "\n".join(lines),
        settings.DEFAULT_FROM_EMAIL,
        [settings.ADMIN_ORDER_EMAIL],
        fail_silently=True,
    )
    items.delete()
    return render(request, "orders/quick_confirmation.html", {"items": sent_items})
