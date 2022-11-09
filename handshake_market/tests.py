# from django.test import TestCase
#
# # Create your tests here.
#
# import decimal
#
# from django.contrib import messages
# from django.shortcuts import render, redirect
#
# from user_auth.models import User
# from .models import Product, PurchaseHistory, SellingHistory, CashIn
# from .forms import CashInForm, PriceUpdateForm
#
# UNSOLD_STATUS = 2
# SOLD_STATUS = 1
#
#
# # Create your views here.
# def home(request):
#     return render(request, 'handshake_market/home.html', {})
#
#
# def is_auth_user(request):
#     return request.user.is_authenticated
#
#
# def cash_in(request):
#     if not is_auth_user(request):
#         return redirect(to='register')
#     if request.method == "POST":
#         current_user = User.objects.get(id=request.user.id)
#         deposit_amount = request.POST['amount']
#         CashIn.objects.create(
#             user_id=current_user,
#             amount=deposit_amount
#         )
#         current_user.balance += decimal.Decimal(request.POST['amount'])
#         current_user.save(update_fields=['balance'])
#
#         return redirect(to='market_page')
#     form = CashInForm()
#     return render(request, 'handshake_market/cash_in.html', {'form': form})
#
#
# def update_product_price_page(request):
#     if not is_auth_user(request):
#         return redirect(to='register')
#     print("Test", request.GET['product_id'])
#     product = Product.objects.get(id=request.GET['product_id'])
#     print(product)
#     form = PriceUpdateForm()
#     return render(request, 'handshake_market/product_update.html', {'product': product, 'form': form})
#
#
# def update_product_price(request):
#     if not is_auth_user(request):
#         return redirect(to='register')
#     product = Product.objects.get(id=request.POST['product_id'])
#     if product.author.id != request.user.id:
#         return redirect(to='market_page')
#
#     product.price = request.POST['amount']
#     product.save(update_fields=['price'])
#
#     return redirect(to='market_page')
#
#
# def sell_product(request):
#     if not is_auth_user(request):
#         return redirect(to='register')
#     product_id = request.POST['sold_item']
#     try:
#         product = Product.objects.get(id=product_id)
#     except Product.DoesNotExist:
#         return redirect(to='market_page')
#
#     if request.user.id != product.author.id or product.status == UNSOLD_STATUS:
#         print("SELL_PRODUCT True False: ", product.status, UNSOLD_STATUS)
#
#         return redirect(to='market_page')
#
#     product.status = UNSOLD_STATUS
#     product.save(update_fields=['status'])
#     return redirect(to='market_page')
#
#
# def purchase_product(request):
#     if not is_auth_user(request):
#         return redirect(to='register')
#     if request.method == "POST":
#         product_id = request.POST['purchased_item']
#         try:
#             product = Product.objects.get(id=product_id)
#         except Product.DoesNotExist:
#             return redirect(to='market_page')
#
#         current_user = User.objects.get(id=request.user.id)
#         if current_user.balance < product.price:
#             return redirect(to='market_page')
#
#         product_owner = User.objects.get(id=product.author.id)
#         SellingHistory.objects.create(
#             user_id=product_owner,
#             product_id=product,
#             amount=product.price
#         )
#
#         product_owner.balance += product.price
#         product_owner.save(update_fields=['balance'])
#
#         PurchaseHistory.objects.create(
#             user_id=current_user,
#             product_id=product,
#             amount=product.price
#         )
#         current_user.balance -= product.price
#         current_user.save(update_fields=['balance'])
#
#         product.status = SOLD_STATUS
#         product.author = current_user
#         product.save(update_fields=['status', 'author'])
#
#     return redirect(to='market_page')
