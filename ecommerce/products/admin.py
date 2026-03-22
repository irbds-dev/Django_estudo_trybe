from django.contrib import admin
from products.models import Product
from products.models import Customer

admin.site.site_header = "E-commerce Admin"
admin.site.register(Product)
admin.site.register(Customer)
