from django.urls import path
from .views import HomePageView, OrdersListView, UsersListView, SearchView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('orders', OrdersListView.as_view(), name='orders'),
    path('users', UsersListView.as_view(), name='users'),
    path('search', SearchView.as_view(), name='search'),
]