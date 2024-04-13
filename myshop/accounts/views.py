from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import CreateView

from orders.models import Order


class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


@login_required
def profile(request):
    user = request.user
    orders = Order.objects.all()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.instance.user = user
            form.save()
            return redirect('profile')
    else:
        form = UserCreationForm()
    return render(request, 'profile.html', {'form': form, 'orders': orders})

class Profile(CreateView):
    template_name = 'profile.html'
    model = User
    form_class = UserCreationForm