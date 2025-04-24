from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from .cart import Cart
from Shop.models import Product
from django.http import JsonResponse
from django.contrib import messages
import json
from django.conf import settings
import requests
import random
import string



DESCRIPTION = "Thank you for purchasing from us"

if settings.SANDBOX:
    sandbox = "sandbox"
else:
    sandbox = "payment"
ZP_API_REQUEST_URL = f"https://{sandbox}.zarinpal.com/pg/v4/payment/request.json"
ZP_API_VERIFY_URL = f"https://{sandbox}.zarinpal.com/pg/v4/payment/verify.json"
ZP_API_STARTPAY_URL = f"https://{sandbox}.zarinpal.com/pg/StartPay/"

callback_url = "http://127.0.0.1:8000/cart/verify"


def payment_zarinpal(request):
    cart = Cart(request)
    amount =  cart.total_price()
    data = {
    "merchant_id": settings.MERCHANT,
    "amount": amount,  # مقدار قیمت محصول باید صحیح باشد
    "currency" : "IRT",
    "description": DESCRIPTION,
    "callback_url": callback_url
}

    res = requests.post(ZP_API_REQUEST_URL,json=data)
    print("*"*100)
    print(res.text)
    print("*"*100)
    if res.status_code == 200:
        response = res.json()
        if response["data"]["code"] == 100:
            authority = response["data"]["authority"]
            url = f"{ZP_API_STARTPAY_URL}{authority}"
            return redirect(url)
        else:
            return HttpResponse("error from Zarinpal Website")
    else:
        return HttpResponse("error from Zarinpal Website")
    
def verify_payment(request):
    cart = Cart(request)
    amount =  cart.total_price()
    authority = request.GET.get("Authority")
    status = request.GET.get("Status")
    data = {
        "merchant_id" : settings.MERCHANT,
        "amount" : amount,
        "authority" : authority,
    }
    if status != "OK":
        return HttpResponse("خرید شما به دلایلی انجام نشد لطفا با پشتیبانی تماس بگیرید")
    res = requests.post(ZP_API_VERIFY_URL,json=data)
    print(res.text)
    
    if res.status_code == 200:
        response = res.json()
        if response["data"]["code"] == 100:
            post_code_for_order = ""
            for i in range(10):
               post_code_for_order += random.choice(string.digits)
            return HttpResponse(f"خرید شما با موفقیت انجام شد کد رهگیری شما :{post_code_for_order}")
        else:
            return HttpResponse(f" پرداخت ناموفق بود {response['data']['message']}")
    else:
        return HttpResponse("خطا در برقراری اتصال به زرین پال")
            
def cart_summary(request):
    cart = Cart(request)
    cart_Productss = cart.get_prods()
    session = cart.get_real_session()


    return render(request,"cart/index.html",{"cart_Productss":cart_Productss, "session": session})
def cart_add(request):    
    if (
        request.method == "POST"
        and request.headers.get("X-Requested-With") == "XMLHttpRequest"
    ):  
        cart = Cart(request)

        Productss_id = request.POST.get("Productss_id")
        Productss_state = request.POST.get("Productss_state")
        situation_state = request.POST.get("situation_state")
        if situation_state == "noting":
            print("Please select your brand")
            return JsonResponse({"error": "Please select state of course"}, status=404)
        if not Productss_id:
            return JsonResponse({"error": "Please select state of course"}, status=404)
        products = get_object_or_404(Product,id=Productss_id)
        cart.add(products = products, state = Productss_state) 
        
        cart_quantity = cart.__len__()
        
        if str(products.is_sale) == "True":
            return JsonResponse({"Productss_Product_name": products.Product_name,"Productss_price" : float(products.sale_price)}) 
        else:
            return JsonResponse({"Productss_Product_name": products.Product_name,"Productss_price" : float(products.price),"Count" : cart_quantity}) 

    else:
        return JsonResponse({"error":"Invalid Request"},status=400)

from django.http import JsonResponse

def cart_update(request):
    cart = Cart(request)
    if request.POST.get("action") == "post":
        Productss_id = request.POST.get("Productss_id")
        Productss_state = request.POST.get("Productss_state")
        Productss_price = None
        product = Product.objects.get(id=Productss_id)
        if product.is_sale:
            Productss_price = product.sale_price
        else:
            Productss_price = product.price

        cart.update(Productss_id,Productss_state,Productss_price)
        response =JsonResponse({"state":Productss_state})
        return response
def cart_delete(request):
    cart = Cart(request)
    Productss_id = request.POST.get("Productss_id")
    products = get_object_or_404(Product,id=Productss_id)
    cart.delete(products)
    return redirect('cart_summary')