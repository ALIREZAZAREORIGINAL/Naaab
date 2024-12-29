from django.urls import path
from .views import helloworld ,about,login_user,logout_user,signup_user,product,category_products,add_to_cart ,cart ,remove_from_cart,update_cart,search,order_report,checkout,profile
from django.urls import path, include


urlpatterns = [
    path('', helloworld, name="home"),  # اضافه کردن ویو به طور مستقیم 
    path('about/',about,name="about"),
    path('login', login_user, name="login"),
    path('logout', logout_user, name="logout"),
    path('signup',signup_user , name = "signup"),
    path('product/<int:pk>',product, name = "product"),
    path('category/<int:pk>/', category_products, name="category_products"),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', cart, name='cart'),
    path('remove-from-cart/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
    path('update-cart/<int:product_id>/', update_cart, name='update_cart'),
    path('search/', search, name='search'), 
    path('checkout/', checkout, name='checkout'),
    path('profile/', profile, name='profile'),





]
