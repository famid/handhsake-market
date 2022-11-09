from django.urls import path
from . import views
urlpatterns = [
    path('user_list/', views.user_list_page, name='user_list'),
    path('purchase_history/<int:user_id>', views.purchase_history_page, name='user_purchase_history'),
    path('selling_history/<int:user_id>', views.selling_history_page, name='user_selling_history'),
    path('cash_in_history/<int:user_id>', views.cash_in_history_page, name='user_cash_in_history'),
    path('transaction/<int:user_id>', views.user_transaction_summary, name='user_transaction_summary')
]