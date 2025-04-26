from django.urls import path
from django.contrib import admin
from .views import HomePageView, OrdersListView, UsersListView, SearchView, OrdersDetailView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('users', UsersListView.as_view(), name='users'),
    path('orders', OrdersListView.as_view(), name='orders'),
    path('search', SearchView.as_view(), name='search'),
    path('orders/<int:pk>', OrdersDetailView.as_view(), name='order_detail'),
]