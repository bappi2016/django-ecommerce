from django.urls import path
from .views import HomeView,ProductDetailView,add_to_cart,remove_from_cart,OrderSummaryView,remove_single_item_from_cart,CheckoutView,PaymentView,AddCouponView,RequestRefundView,add_to_wishlist,WishlistView

app_name = 'core'

urlpatterns = [

    path('',HomeView.as_view(),name='home'),
    path('product/<slug>/',ProductDetailView.as_view(),name='product_detail'),
    path('order-summary/',OrderSummaryView.as_view(),name='order-summary'),
    path('wishlist/',WishlistView.as_view(),name='wishlist'),
    path('add-to-cart/<slug>/',add_to_cart,name='add-to-cart'),
    path('add-coupon/',AddCouponView.as_view(),name='add-coupon'),
    path('remove-from-cart/<slug>/',remove_from_cart,name='remove-from-cart'),
    path('remove-the-single-item/<slug>/',remove_single_item_from_cart,name='remove-the-single-item'),
    path('checkout/',CheckoutView.as_view(),name='checkout'),
    path('payment/<payment_option>/',PaymentView.as_view(),name='payment'),
    path('request-refund/',RequestRefundView.as_view(),name='request-refund'),
    path('add-to-wishlist/<slug>/',add_to_wishlist,name='add-to-wishlist')

]