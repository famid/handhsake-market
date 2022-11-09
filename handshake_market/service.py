import decimal

from user_auth.models import User
from .models import Product, PurchaseHistory, SellingHistory, CashIn

UNSOLD_STATUS = 2
SOLD_STATUS = 1


def is_auth_user(request):
    return request.user.is_authenticated


def market_page_service(request):
    if not is_auth_user(request):
        return dict(success=False, message="unauthorized, 401", data=None)

    current_user = request.user

    try:
        available_items = Product.objects.filter(status=UNSOLD_STATUS)
        user_owned_items = Product.objects.filter(
            author=current_user.id, status=SOLD_STATUS
        )
    except Product.DoesNotExist as error:
        return dict(success=False, message=str(error), data=None)

    data = {"items": available_items, "owned_items": user_owned_items}

    return dict(success=True, message=None, data=data)


def cash_in_service(request) -> dict:
    if not is_auth_user(request):
        return dict(success=False, message="unauthorized, 401", data=None)

    try:
        current_user = User.objects.get(id=request.user.id)
    except User.DoesNotExist as error:
        return dict(success=False, message=str(error), data=None)

    deposit_amount = request.POST["amount"]

    try:
        CashIn.objects.create(user_id=current_user, amount=deposit_amount)
    except Exception as error:
        return dict(success=False, message=str(error), data=None)

    current_user.balance += decimal.Decimal(request.POST["amount"])
    current_user.save(update_fields=["balance"])

    return dict(success=True, message="Balance is added successfully", data=None)
    pass


def update_product_price_service(request) -> dict:
    if not is_auth_user(request):
        return dict(success=False, message="unauthorized, 401", data=None)
    try:
        product = Product.objects.get(id=request.POST["product_id"])
    except Product.DoesNotExist as error:
        return dict(success=False, message=str(error), data=None)

    new_price_to_set = request.POST["amount"]
    product.price = new_price_to_set
    product.save(update_fields=["price"])

    return dict(
        success=True, message="Product price is updated successfully", data=None
    )
    pass


def sell_product_service(request):
    if not is_auth_user(request):
        return dict(success=False, message="unauthorized, 401", data=None)

    product_id = request.POST["sold_item"]
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist as error:
        return dict(success=False, message=str(error), data=None)

    if request.user.id != product.author.id or product.status == UNSOLD_STATUS:
        return dict(success=False, message="This product can not be sold", data=None)

    try:
        product.status = UNSOLD_STATUS
        product.save(update_fields=["status"])
    except Exception as error:
        return dict(success=False, message=str(error), data=None)

    return dict(success=True, message="Product is sold successfully", data=None)
    pass


def purchase_product_response(request):
    if not is_auth_user(request):
        return dict(success=False, message="unauthorized, 401", data=None)
    product_id = request.POST["purchased_item"]
    try:
        product = Product.objects.get(id=product_id)
        current_user = User.objects.get(id=request.user.id)
    except Product.DoesNotExist as error:
        return dict(success=False, message=str(error), data=None)

    if current_user.balance < product.price:
        return dict(
            success=False, message="Does not have sufficient balance!!", data=None
        )

    try:
        product_owner = User.objects.get(id=product.author.id)
        SellingHistory.objects.create(
            user_id=product_owner, product_id=product, amount=product.price
        )

        product_owner.balance += product.price
        product_owner.save(update_fields=["balance"])

        PurchaseHistory.objects.create(
            user_id=current_user, product_id=product, amount=product.price
        )
        current_user.balance -= product.price
        current_user.save(update_fields=["balance"])

        product.status = SOLD_STATUS
        product.author = current_user
        product.save(update_fields=["status", "author"])
    except Exception as error:
        return dict(success=False, message=str(error), data=None)

    return dict(success=True, message="Product is purchased successfully", data=None)
