from django.urls import path
from . import views



urlpatterns = [
    path('', views.store, name='store'),
    path('buy-item/<name>/', views.buy_item, name='buy_item'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    # path('deposit/', views.deposit, name="deposit"),
    # path('deposited/', views.deposit_complete, name='deposit_detail'),
    path('initiate-payment/', views.initiate_payment, name='initiate-payment'),
    path('initiate-payment/<str:ref>', views.verify_payment, name='verify-payment'),
]