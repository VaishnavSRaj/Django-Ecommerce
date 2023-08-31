from django.urls import path

from Ecommerce_app import views

app_name = 'Ecommerce_app'

# 1. The first route ('') is the default homepage and is associated with the view function
# "allProductCategory," which shows all available products from all categories.
# 2. The second route ('<slug:category_slug>/') expects a category slug in the URL
# and is also associated with the view function "allProductCategory," which filters and
# displays products specific to the given category slug.

urlpatterns = [

    path('', views.allProductCategory, name='allProducts'),
    path('<slug:category_slug>/', views.allProductCategory, name='product_by_category'),
    path('<slug:category_slug>/<slug:product_slug>/', views.product_detail, name='product_detail')

]
