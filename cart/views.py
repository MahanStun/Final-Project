from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.conf import settings

import requests
import random
import string

from .cart import *
from .models import Order
from Shop.models import Product
from dashboard.models import Product_dashboard

# تنظیمات زرین‌پال
DESCRIPTION = "Thank you for purchasing from us"
sandbox = "sandbox" if settings.SANDBOX else "payment"
ZP_API_REQUEST_URL = f"https://{sandbox}.zarinpal.com/pg/v4/payment/request.json"
ZP_API_VERIFY_URL = f"https://{sandbox}.zarinpal.com/pg/v4/payment/verify.json"
ZP_API_STARTPAY_URL = f"https://{sandbox}.zarinpal.com/pg/StartPay/"
callback_url = "http://127.0.0.1:8000/cart/verify/"

# 🚀 ۱. ارسال درخواست پرداخت به زرین‌پال
def payment_zarinpal(request):
    cart = Cart(request)
    amount = cart.total_price()

    data = {
        "merchant_id": settings.MERCHANT,
        "amount": amount,
        "currency": "IRT",
        "description": DESCRIPTION,
        "callback_url": callback_url
    }

    res = requests.post(ZP_API_REQUEST_URL, json=data)

    if res.status_code == 200:
        response = res.json()
        if response["data"]["code"] == 100:
            authority = response["data"]["authority"]
            url = f"{ZP_API_STARTPAY_URL}{authority}"
            return redirect(url)
        else:
            return HttpResponse(f"خطا از سمت زرین‌پال: {response['data']['message']}")
    else:
        return HttpResponse("خطا در ارتباط با زرین‌پال")


# ✅ ۲. تأیید پرداخت و ثبت سفارش





def verify_payment(request):
    cart = Cart2(request)
    amount = cart.total_price()
    authority = request.GET.get("Authority")
    status = request.GET.get("Status")

    if not authority or status != "OK":
        return HttpResponse("❌ خرید شما انجام نشد، لطفاً با پشتیبانی تماس بگیرید.")

    data = {
        "merchant_id": settings.MERCHANT,
        "amount": amount,
        "authority": authority,
    }

    res = requests.post(ZP_API_VERIFY_URL, json=data)
    if res.status_code == 200:
        response = res.json()
        if response["data"]["code"] == 100:
            cart_data = cart.cart
            product_ids = cart_data.keys()
            products = Product_dashboard.objects.filter(id__in=product_ids)

            if not products:
                return HttpResponse("سبد خرید شما خالی است یا محصولات یافت نشد!")

            tracking_code = "".join(random.choices(string.digits, k=10))

            for product in products:
                Order.objects.create(
                    user=request.user,
                    product=product,
                    tracking_code=tracking_code,
                    is_paid=True
                )

            cart.clear()  # 🛒 سبد خرید پاک می‌شود!

            return render(request, "cart/payment_success.html", { 
                "orders": products, 
                "tracking_code": tracking_code 
            })
        else:
            return HttpResponse(f"پرداخت ناموفق بود: {response['data']['message']}")
    else:
        return HttpResponse("خطا در اتصال به درگاه زرین‌پال")




# 🔎 ۳. نمایش سفارش با کد رهگیری
def get_products_by_tracking_code(request):
    context = {}

    if request.method == "POST":
        tracking_code = request.POST.get("tracking_code", "").strip()
        orders = Order.objects.filter(tracking_code=tracking_code)

        if orders.exists():
            context["orders"] = orders
        else:
            context["error"] = "هیچ سفارشی با این کد رهگیری پیدا نشد."

    return render(request, "cart/products_by_tracking.html", context)



# 🛒 نمایش سبد خرید
def cart_summary(request):
    cart = Cart(request)
    cart_Productss = cart.get_prods()
    session = cart.get_real_session()

    return render(request, "cart/index.html", {"cart_Productss": cart_Productss, "session": session})

# ➕ افزودن محصول به سبد خرید
def cart_add(request):    
    if request.method == "POST" and request.headers.get("X-Requested-With") == "XMLHttpRequest":  
        cart = Cart(request)

        Productss_id = request.POST.get("Productss_id")
        Productss_state = request.POST.get("Productss_state")

        if not Productss_id:
            return JsonResponse({"error": "لطفاً محصول را انتخاب کنید."}, status=404)

        products = get_object_or_404(Product_dashboard, id=Productss_id)
        cart.add(products=products, state=Productss_state)

        print("Updated Cart:", cart.cart)  # نمایش سبد خرید بعد از افزودن محصول


        cart_quantity = cart.__len__()

        return JsonResponse({
            "Productss_name": products.name,
            "Productss_price": float(products.sale_price) if products.is_sale else float(products.price),
            "Count": cart_quantity
        })

    else:
        return JsonResponse({"error": "درخواست نامعتبر"}, status=400)

# 📝 بروزرسانی سبد خرید
def cart_update(request):
    cart = Cart(request)
    if request.POST.get("action") == "post":
        Productss_id = request.POST.get("Productss_id")
        Productss_state = request.POST.get("Productss_state")

        product = get_object_or_404(Product_dashboard, id=Productss_id)
        Productss_price = product.sale_price if product.is_sale else product.price

        cart.update(Productss_id, Productss_state, Productss_price)
        response = JsonResponse({"state": Productss_state})
        return response

# ❌ حذف محصول از سبد خرید
def cart_delete(request):
    cart = Cart(request)
    Productss_id = request.POST.get("Productss_id")
    products = get_object_or_404(Product_dashboard, id=Productss_id)
    cart.delete(products)
    return redirect('cart_summary')



