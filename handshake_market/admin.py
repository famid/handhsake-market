from django.contrib import admin
from .models import Product, PurchaseHistory, SellingHistory, CashIn


admin.site.register(Product)
admin.site.register(PurchaseHistory)
admin.site.register(SellingHistory)
admin.site.register(CashIn)
