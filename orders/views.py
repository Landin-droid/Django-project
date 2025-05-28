from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import OrderItem, Order
from .forms import OrderCreateForm
from cart.cart import Cart


@login_required
def order_create(request):
    cart = Cart(request)
    if not cart:  # Проверяем, не пуста ли корзина
        return redirect('LabStart:all_product_list')  # Перенаправляем, если корзина пуста

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            # Создаём заказ
            order = form.save(commit=False)
            order.user = request.user  # Устанавливаем текущего пользователя
            order.order_date = timezone.now()  # Устанавливаем текущую дату
            order.created_at = timezone.now()
            order.updated_at = timezone.now()
            order.status = Order.Status.PENDING  # Устанавливаем статус "В ожидании"
            order.save()  # Сохраняем заказ

            # Переносим товары из корзины в OrderItem
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    name=item['product'].name,
                    price=item['price'],
                    quantity=item['quantity']
                )

            # Очищаем корзину
            cart.clear()

            # Перенаправляем на страницу подтверждения заказа (нужно создать)
            return redirect('orders:order_detail', order_id=order.order_id)
    else:
        form = OrderCreateForm()

    return render(request, 'order_create.html', {'form': form, 'cart': cart})

def order_detail(request, order_id):
    order = get_object_or_404(Order, order_id=order_id, user=request.user)
    return render(request, 'order_detail.html', {'order': order})