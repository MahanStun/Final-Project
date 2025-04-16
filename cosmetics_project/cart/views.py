from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from .cart import Cart
from Shop.models import Product
from django.http import JsonResponse
from django.contrib import messages
import json



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
        Book_count = request.POST.get("Productss_count")
        situation_state = request.POST.get("situation_state")
        if situation_state == "noting":
            print("Please select the language you want your book to be in")
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

        
def cart_delete(request):
    cart = Cart(request)
    Productss_id = request.POST.get("Productss_id")
    products = get_object_or_404(Product,id=Productss_id)
    cart.delete(products)
    return redirect('cart_summary')