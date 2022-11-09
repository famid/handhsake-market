import logging

from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Sum
from django.shortcuts import render

from handshake_market.models import PurchaseHistory, SellingHistory, CashIn
from user_auth.models import User


def user_list_page(request):
    user_list = User.objects.filter(is_superuser=False, is_staff=False)
    users = paginate_helper(request, user_list)
    data = {"users": users}

    return render(request, "ledger/user_list.html", data)


def user_transaction_summary(request, user_id):
    template_name = "ledger/purchase_history.html"
    try:
        total_purchase_amount = PurchaseHistory.objects.filter(
            user_id=user_id
        ).aggregate(TOTAL=Sum("amount"))["TOTAL"]
        total_selling_amount = SellingHistory.objects.filter(user_id=user_id).aggregate(
            TOTAL=Sum("amount")
        )["TOTAL"]
        total_cash_in_amount = CashIn.objects.filter(user_id=user_id).aggregate(
            TOTAL=Sum("amount")
        )["TOTAL"]
        current_balance = User.objects.get(id=user_id).balance
    except Exception as error:
        logging.debug(error)
        messages.error(request, "Something went wrong!!")
        return render(request, template_name, {})

    data = {
        "total_purchase_amount": total_purchase_amount,
        "total_selling_amount": total_selling_amount,
        "total_cash_in_amount": total_cash_in_amount,
        "current_balance": current_balance,
    }

    return render(request, template_name, data)


def purchase_history_page(request, user_id):
    purchase_history_list = PurchaseHistory.objects.filter(user_id=user_id)
    purchase_history = paginate_helper(request, purchase_history_list)
    data = {"entries": purchase_history}

    return render(request, "ledger/purchase_history.html", data)


def selling_history_page(request, user_id):
    selling_history_list = SellingHistory.objects.filter(user_id=user_id)
    selling_history = paginate_helper(request, selling_history_list)
    data = {"entries": selling_history}

    return render(request, "ledger/selling_history.html", data)


def cash_in_history_page(request, user_id):
    cash_in_history_list = CashIn.objects.filter(user_id=user_id)
    cash_in_history = paginate_helper(request, cash_in_history_list)
    data = {"entries": cash_in_history}

    return render(request, "ledger/cash_in_history.html", data)


def paginate_helper(request, query_data, pagination_number=5):
    page = request.GET.get("page", 1)
    paginator = Paginator(query_data, pagination_number)

    try:
        query_paginated_data = paginator.page(page)
    except PageNotAnInteger:
        query_paginated_data = paginator.page(1)
    except EmptyPage:
        query_paginated_data = paginator.page(paginator.num_pages)

    return query_paginated_data
