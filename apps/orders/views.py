from django.conf import settings
from django.core.mail import send_mail
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from apps.cart.services import get_or_create_cart
from .forms import CheckoutForm
from .models import Customer, Order, OrderItem


def checkout(request):
    cart = get_or_create_cart(request)
    items = cart.items.select_related("product")

    if not items.exists():
        return redirect("shop")

    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                customer = Customer.objects.create(
                    full_name=form.cleaned_data["full_name"],
                    phone=form.cleaned_data["phone"],
                    address=form.cleaned_data["address"],
                    city=form.cleaned_data["city"],
                )
                order = Order.objects.create(
                    customer=customer,
                    status="PENDING",
                    message=form.cleaned_data.get("message", ""),
                )
                total = 0
                for item in items:
                    OrderItem.objects.create(
                        order=order,
                        product=item.product,
                        product_name=item.product.name,
                        unit_price=item.product.price,
                        quantity=item.quantity,
                        line_total=item.product.price * item.quantity,
                    )
                    total += item.product.price * item.quantity
                    if item.product.stock >= item.quantity:
                        item.product.stock -= item.quantity
                        item.product.save()
                order.total_amount = total
                order.save()
                items.delete()
            subject = f"Nouvelle commande #{order.id} - Doriane World"
            lines = [
                f"Client: {customer.full_name}",
                f"Telephone: {customer.phone}",
                f"Adresse: {customer.address}, {customer.city}",
                f"Message: {order.message or '-'}",
                "",
                "Produits:",
            ]
            for item in order.items.all():
                lines.append(f"- {item.product_name} x {item.quantity} = {item.line_total} EUR")
            lines.append("")
            lines.append(f"Total: {order.total_amount} EUR")
            # Email notification disabled - using WhatsApp only
            # send_mail(
            #     subject,
            #     "\n".join(lines),
            #     settings.DEFAULT_FROM_EMAIL,
            #     [settings.ADMIN_ORDER_EMAIL],
            #     fail_silently=True,
            # )
            return redirect("order_confirmation", order_id=order.id)
    else:
        form = CheckoutForm()

    total = sum(item.product.price * item.quantity for item in items)
    return render(request, "orders/checkout.html", {"form": form, "items": items, "total": total})


def confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, "orders/confirmation.html", {"order": order})
