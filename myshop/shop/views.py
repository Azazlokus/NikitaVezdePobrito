from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from cart.forms import CartAddProductForm
from django.views.generic import ListView

from .models import Category, Product


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request,
                  'shop/product/list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products})


def product_detail(request, id, slug):
    product = get_object_or_404(Product,
                                id=id,
                                slug=slug,
                                available=True)
    cart_product_form = CartAddProductForm()
    return render(request,
                  'shop/product/detail.html',
                  {'product': product,
                   'cart_product_form': cart_product_form})


class SearchView(ListView):
    template_name = 'shop/product/detail.html'
    model = Product
    context_object_name = "list_of_all_orders"

    def get_queryset(self):
        query = self.request.GET.get('q')
        return Product.objects.filter(
            Q(customer__first_name__icontains=query) | Q(customer__last_name__icontains=query)
        )
