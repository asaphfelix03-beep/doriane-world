from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404
from apps.orders.models import Order


@staff_member_required
def order_list(request):
    if request.method == "POST":
        order_id = request.POST.get("order_id")
        status = request.POST.get("status")
        order = get_object_or_404(Order, id=order_id)
        order.status = status
        order.save()
        return redirect("dashboard_orders")

    orders = Order.objects.select_related("customer").prefetch_related("items").order_by("-created_at")
    return render(
        request,
        "dashboard/order_list.html",
        {"orders": orders, "status_choices": Order.STATUS_CHOICES},
    )
