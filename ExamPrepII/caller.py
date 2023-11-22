import os
import django
from django.db.models import Q, Count, F

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()


from main_app.models import Profile, Product, Order


def get_profiles(search_string=None):
    matched_profiles = None

    if search_string is not None:
        q = Q(full_name__icontains=search_string) | Q(email__icontains=search_string) | Q(phone_number__icontains=search_string)

        matched_profiles = Profile.objects.filter(q).order_by("full_name").annotate(orders_count=Count("profile_orders"))

    if not matched_profiles:
        return ""

    profile_info = [
        f"Profile: {p.full_name}, email: {p.email}, phone number: {p.phone_number}, orders: {p.orders_count}"
        for p in matched_profiles
    ]

    return "\n".join(profile_info)


def get_loyal_profiles():
    loyal_profiles = Profile.objects.get_regular_customers().annotate(orders_count=Count("profile_orders"))

    if not loyal_profiles:
        return ""

    profile_info = [
        f"Profile: {p.full_name}, orders: {p.orders_count}"
        for p in loyal_profiles
    ]

    return "\n".join(profile_info)


def get_last_sold_products():
    latest_order = Order.objects.order_by("-creation_date", "products__name").first()

    if latest_order is None or not Product.objects.all():
        return ""

    return f"Last sold products: {', '.join([p.name for p in latest_order.products.all()])}"


def get_top_products():
    top_products = (Product.objects.
                    prefetch_related("product_orders").
                    annotate(orders_count=Count("product_orders")).
                    filter(orders_count__gt=0).
                    order_by("-orders_count", "name"))[:5]

    if top_products is None or not Order.objects.all():
        return ""

    product_info = ["Top products:"]

    for p in top_products:
        product_info.append(f"{p.name}, sold {p.orders_count} times")

    return "\n".join(product_info)


def apply_discounts():
    orders = (Order.objects.
              annotate(products_count=Count("products")).
              filter(is_completed=False, products_count__gt=2).
              update(total_price=F("total_price") * 0.90))

    return f"Discount applied to {orders} orders."


def complete_order():
    oldest_order = Order.objects.order_by("creation_date").filter(is_completed=False).first()

    if oldest_order is None:
        return ""

    oldest_order.is_completed = True
    oldest_order.save()

    for p in oldest_order.products.all():
        p.in_stock -= 1

        if p.in_stock <= 0:
            p.is_available = False

        p.save()

    return "Order has been completed!"





