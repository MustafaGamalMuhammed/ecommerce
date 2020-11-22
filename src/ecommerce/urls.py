from django.urls import path
from ecommerce import views


authentication_urlpatterns = [
    path('signup/', views.signup, name="signup"),
    path('signin/', views.signin, name="signin"),
]

home_urlpatterns = [
    path('', views.home, name="home"),
]

shop_urlpatterns = [
    path('shop/', views.shop, name="shop"),
]

product_urlpatterns = [
    path('product/', views.product, name="product"),
]

cart_urlpatterns = [
    path('cart/', views.cart, name="cart"),
]

urlpatterns = []
urlpatterns.extend(authentication_urlpatterns)
urlpatterns.extend(shop_urlpatterns)
urlpatterns.extend(product_urlpatterns)
urlpatterns.extend(cart_urlpatterns)
urlpatterns.extend(home_urlpatterns)