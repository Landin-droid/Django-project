from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, UserUpdateForm
from django.views.generic import TemplateView, DetailView
from django.views.generic.list import ListView
from LabStartApp.models import Order, User

class HomePageView(TemplateView):
    template_name = 'home.html'

class UsersListView(ListView):
    template_name = "users.html"
    model = User
    context_object_name = 'list_of_all_users'

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def profile_view(request):
    user = request.user
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=user)

    return render(request, 'profile.html', {'form': form})
class OrdersListView(ListView):
    template_name = "orders.html"
    model = Order
    context_object_name = 'list_of_all_orders'

class OrdersDetailView(DetailView):
    template_name = "order_detail.html"
    model = Order
    context_object_name = 'order'

class SearchView(ListView):
    template_name = "search.html"
    model = Order
    context_object_name = 'list_of_all_orders'

    def get_queryset(self):
        query = self.request.GET.get('q')

        if not query:
            return Order.objects.none()

        return Order.objects.filter(
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query) |
            Q(user__first_name__icontains=query.split()[0], user__last_name__icontains=query.split()[-1])
        ).order_by('-order_date')