
from django.core.mail import send_mail
from django.shortcuts import render
from django.template.defaultfilters import date

from .models import OrderItem, Order
from .forms import OrderCreateForm
from cart.cart import Cart


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST, user=request.user)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            # clear the cart
            cart.clear()
            # launch asynchronous task
            order1 = Order.objects.get(id=order.id)
            subject = f'Заказ номер {order1.id}'
            message = f'Дорогой {order1.first_name},\n\n' \
                      f'Вы успешно оформили заказ \n\n' \
                      f'Номер вашего заказа: {order1.id} от {date(order.created, "Y-m-d")}.'
            mail_sent = send_mail(subject,
                                  message,
                                  'abk19@tpu.ru',
                                  [order1.email],
                                  fail_silently=False,
                                  )
            return render(request,
                          'orders/order/created.html',
                          {'order': order1})
    else:
        form = OrderCreateForm(user=request.user)
    return render(request,
                  'orders/order/create.html',
                  {'cart': cart, 'form': form})
