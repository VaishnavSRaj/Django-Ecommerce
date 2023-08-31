from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, InvalidPage, EmptyPage

from Ecommerce_app.models import Category, Product


# Create your views here.

# This function called "allProductCategory" takes a request and an optional category_slug
# as input, and it retrieves products from the database that belong to a specific category
# (if category_slug is provided)or all available products (if category_slug is not provided).
# It then renders a webpage using the "category.html"template, displaying the category and the
# corresponding products.

def allProductCategory(request, category_slug=None):
    category_page = None
    products_list = None
    if category_slug != None:
        category_page = get_object_or_404(Category, slug=category_slug)
        products_list = Product.objects.all().filter(category=category_page, available=True)
    else:
        products_list = Product.objects.all().filter(available=True)
    paginator = Paginator(products_list, 6)
    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1
    try:
        products = paginator.page(page)
    except (EmptyPage, InvalidPage):
        products = paginator.page(paginator.num_pages)

    return render(request, 'category.html', {'category': category_page, 'products': products})


def product_detail(request, category_slug, product_slug):
    try:
        product = Product.objects.get(category__slug=category_slug, slug=product_slug)
    except Exception as e:
        raise e
    return render(request, 'product_detail.html', {'product': product})
