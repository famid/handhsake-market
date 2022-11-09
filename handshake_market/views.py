from django.shortcuts import render, redirect

from .forms import CashInForm, PriceUpdateForm
from django.contrib import messages
from .models import Product
from .service import (
    market_page_service,
    cash_in_service,
    is_auth_user,
    update_product_price_service,
    sell_product_service,
    purchase_product_response,
)


def home(request):
    template_name = "handshake_market/home.html"
    return render(request, template_name, {})


def market_page(request):
    market_service_response = market_page_service(request)

    if not market_service_response["success"]:
        messages.error(request, market_service_response["message"])
        return redirect(to="register")

    template_name = "handshake_market/market.html"
    return render(request, template_name, market_service_response["data"])


def cash_in(request):
    if request.method == "POST":
        form = CashInForm(request.POST)
        if not form.is_valid():
            messages.error(request, form.errors)
            return redirect(to="market_page")

        cash_in_service_response = cash_in_service(request)
        if not cash_in_service_response["success"]:
            messages.error(request, cash_in_service_response["message"])
            return redirect(to="market_page")

        messages.success(request, cash_in_service_response["message"])
        return redirect(to="market_page")

    template_name = "handshake_market/cash_in.html"
    form = CashInForm()
    return render(request, template_name, {"form": form})


def update_product_price_page(request):
    if not is_auth_user(request):
        return redirect(to="register")
    print("page", request.GET)
    product = Product.objects.get(id=request.GET["product_id"])
    form = PriceUpdateForm()
    return render(
        request,
        "handshake_market/product_update.html",
        {"product": product, "form": form},
    )


def update_product_price(request):
    form = PriceUpdateForm(request.POST)
    if not form.is_valid():
        messages.error(request, form.errors)
        return redirect(to="market_page")
    update_price_response = update_product_price_service(request)
    if not update_price_response["success"]:
        messages.error(request, update_price_response["message"])
        return redirect(to="market_page")

    messages.success(request, update_price_response["message"])
    return redirect(to="market_page")


def sell_product(request):
    product_selling_response = sell_product_service(request)
    if not product_selling_response["success"]:
        messages.error(request, product_selling_response["message"])
        return redirect(to="market_page")

    messages.success(request, product_selling_response["message"])
    return redirect(to="market_page")


def purchase_product(request):
    product_purchase_response = purchase_product_response(request)

    if not product_purchase_response["success"]:
        messages.error(request, product_purchase_response["message"])
        return redirect(to="market_page")

    messages.success(request, product_purchase_response["message"])
    return redirect(to="market_page")
