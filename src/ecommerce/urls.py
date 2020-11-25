from django.urls import path
from ecommerce import views


authentication_urlpatterns = [
    path('signup/', views.signup, name="signup"),
    path('signin/', views.signin, name="signin"),
    path('logout/', views.logout, name="logout"),
]

home_urlpatterns = [
    path('', views.home, name="home"),
]

shop_urlpatterns = [
    path('shop/', views.shop, name="shop"),
]

product_urlpatterns = [
    path('product/<int:id>/', views.product, name="product"),
    path('products/', views.products, name="products"),
    path('get_product/<int:id>/', views.get_product, name="get_product"),
]

cart_urlpatterns = [
    path('cart/', views.cart, name="cart"),
    path('get_cart/', views.get_cart, name="get_cart"),
    path('add_to_cart/<int:id>/', views.add_to_cart, name="add_to_cart"),
]

likes_urlpatterns = [
    path('likes/', views.likes, name="likes"),
    path('get_likes/', views.get_likes, name="get_likes"),
    path('like/<int:id>/', views.like, name="like"),
]

urlpatterns = []
urlpatterns.extend(authentication_urlpatterns)
urlpatterns.extend(shop_urlpatterns)
urlpatterns.extend(product_urlpatterns)
urlpatterns.extend(cart_urlpatterns)
urlpatterns.extend(home_urlpatterns)
urlpatterns.extend(likes_urlpatterns)