from django.urls import path
from .views import home,signup_view,login_view,logout_view,buy_view,notify_admin,phone_request_view,verify_code_view,account_view,buy_product,admin_orders_view,my_orders,send_tg
from .views import API_view1,API_view2,ovqatlar_view,ichimliklar_view,ximya_view,login_required_redirect,kolbasalar_view,sut_view,sabzavotlar_view,mevalar_view,nonlar_view

urlpatterns=[
    path('',home,name="saxifa"),
    path("api1/product", API_view1.as_view(), name="product_api"),
    path("api1/order", API_view2.as_view(), name="order_api"),
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='sign'),
    path('logout/', logout_view, name='logout'),
    path('phone/', phone_request_view, name='phone'),
    path('verify/', verify_code_view, name='verify'),
    path('buy/', buy_view, name='buy'),
    path('notify-admin/', notify_admin, name='notify_admin'),
    path('hisob/', account_view, name='hisob'),
    path("buy_pro/", buy_product, name="buy_pro"),
    path('zakazlar/', admin_orders_view, name='admin_orders'),
    path('my-orders/', my_orders, name='my_orders'),
    path('ximya/', ximya_view, name='ximya'),
    path('ichimliklar/', ichimliklar_view, name='ichimliklar'),
    path('ovqatlar/', ovqatlar_view, name='ovqatlar'),
    path('login-required/',login_required_redirect, name='auth_required'),
    path('kolbasalar/', kolbasalar_view, name='kolbasalar'),
    path('sut/', sut_view, name='sut'),
    path('sabzavotlar/', sabzavotlar_view, name='sabzavotlar'),
    path('mevalar/', mevalar_view, name='mevalar'),
    path('nonlar/', nonlar_view, name='nonlar'),
    path("register/", send_tg, name="register"),
]