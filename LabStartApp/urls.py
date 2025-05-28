from django.contrib.auth import views as auth_views
from django.urls import path
from .views import HomePageView, OrdersListView, UsersListView, SearchView, OrdersDetailView, register, profile_view, \
    AllProductList
from .forms import EmailAuthenticationForm

app_name = 'LabStart'
urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('users', UsersListView.as_view(), name='users'),
    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(
        template_name='registration/login.html',
        authentication_form=EmailAuthenticationForm),
        name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', profile_view, name='profile'),
    path('orders', OrdersListView.as_view(), name='orders'),
    path('search', SearchView.as_view(), name='search'),
    path('orders/<int:pk>', OrdersDetailView.as_view(), name='order_detail'),
    path('products/', AllProductList.as_view(), name='all_product_list'),
]