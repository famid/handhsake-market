from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('market/', views.market_page, name='market_page'),
    path('purchase_product/', views.purchase_product, name='purchase_product'),
    path('sell_product/', views.sell_product, name='sell_product'),
    path('cash_in/', views.cash_in, name='cash_in'),
    path('update_price_page/', views.update_product_price_page, name='update_price_page'),
    path('update_price/', views.update_product_price, name='update_price'),
]