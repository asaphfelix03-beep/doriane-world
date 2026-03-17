from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from .models import Product, Category


def home(request):
    categories = Category.objects.all()
    popular_products = Product.objects.filter(is_popular=True)[:8]
    promo_products = Product.objects.filter(is_promo=True)[:8]
    return render(
        request,
        "home.html",
        {
            "categories": categories,
            "popular_products": popular_products,
            "promo_products": promo_products,
        },
    )


def shop(request):
    products = Product.objects.select_related("category").all()
    query = request.GET.get("q", "").strip()
    if query:
        products = products.filter(
            Q(name__icontains=query)
            | Q(description__icontains=query)
            | Q(category__name__icontains=query)
        )
    categories = Category.objects.all()
    return render(
        request,
        "shop.html",
        {"products": products, "categories": categories, "q": query},
    )


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category)
    query = request.GET.get("q", "").strip()
    if query:
        products = products.filter(
            Q(name__icontains=query)
            | Q(description__icontains=query)
        )
    categories = Category.objects.all()
    return render(
        request,
        "shop.html",
        {
            "products": products,
            "categories": categories,
            "active_category": category,
            "q": query,
        },
    )


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    related_products = (
        Product.objects.filter(category=product.category)
        .exclude(id=product.id)
        .select_related("category")[:4]
    )
    return render(
        request,
        "product_detail.html",
        {"product": product, "related_products": related_products},
    )
