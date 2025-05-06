from django.urls import path
from store import views
from .views import create_payos_order, payos_callback, payment_status

app_name = "store"

urlpatterns = [
    path("", views.index, name="index"),
    path("shop/", views.shop, name="shop"),
    path("category/<id>/", views.category, name="category"),
    path("detail/<slug>/", views.product_detail, name="product_detail"),
    path("cart/", views.cart, name="cart"),
    path("create_order/", views.create_order, name="create_order"),
    path("checkout/<order_id>/", views.checkout, name="checkout"),
    path("coupon_apply/<order_id>/", views.coupon_apply, name="coupon_apply"),
    path("payment_status/<order_id>/", views.payment_status, name="payment_status"),

    path("filter_products/", views.filter_products, name="filter_products"),
    path("add_to_cart/", views.add_to_cart, name="add_to_cart"),
    path("delete_cart_item/", views.delete_cart_item, name="delete_cart_item"),

    path('payment/create_payos_order/<str:order_id>/', create_payos_order, name='store_create_payos_order'),
    path("payment_status/<order_id>/", payment_status, name="payment_status"),
    
    path("order_tracker_page/", views.order_tracker_page, name="order_tracker_page"),
    path("order_tracker_detail/<item_id>/", views.order_tracker_detail, name="order_tracker_detail"),

    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("faqs/", views.faqs, name="faqs"),
    path("privacy_policy/", views.privacy_policy, name="privacy_policy"),
    path("terms_conditions/", views.terms_conditions, name="terms_conditions"),

]