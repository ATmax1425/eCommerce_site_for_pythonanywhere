from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('auth/sign-up/', views.sign_up, name='sign_up'),
    path('after-login/', views.after_login, name='after_login'),
    path('grinding-wheels/', views.grinding_wheels, name="GW"),
    path('hand-gloves/', views.hand_gloves, name="HG"),
    path('safety-equipment/', views.safety_equipment, name="SE"),
    path('product-detail/<str:product_name>', views.product_detail, name="product_detail"),
    path('cart/<item_id>', views.cart, name="cart"),
    path('cart/', views.cart),
    path('create-products/', views.create_products, name="create_products"),
    path('contact', views.contact, name="contact")
]
