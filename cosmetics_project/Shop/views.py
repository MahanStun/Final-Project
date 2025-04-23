from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm, UserChangeForm
from django.urls import reverse_lazy
from django.views import generic
from .models import *
from .forms import *
import random
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import SignUpForm
# Create your views here.



def index_shop(request):
    Products = Product.objects.all()
    return render(request, "shop/index.html", {"Products": Products})
    #return HttpResponse("welcome")
def Products_Cosmetics(request, pk):
    Productss = Product.objects.get(id=pk)
    return render(request, "shop/Products_Cosmetics.html", {"Productss": Productss})


def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # EmailConfirmation(request, username, emailto,)
            messages.success(request, ("با موفقیت وارد اکانت شدید"))
            return redirect("index_shop")
        
        else:
            messages.error(request, ("ورود با خطا مواجه شده است"))
            return redirect("login_url")

    else:
        return render(request, "Shop/login.html")
    
def forgot_password(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        
        try:
            user = User.objects.get(username=username, email=email)  # بررسی صحت نام کاربری و ایمیل
            code = str(random.randint(100000, 999999))  # تولید کد تصادفی
            request.session['reset_code'] = code  # ذخیره در نشست
            request.session['user_email'] = email  # ذخیره ایمیل برای مرحله بعد
            
            send_mail(
                'کد تأیید ورود',
                f'کد تأیید شما: {code}',
                'your_email@example.com',  # ایمیل ارسال‌کننده
                [email],
                fail_silently=False,
            )
            return redirect("verify_reset")  # انتقال به صفحه وارد کردن کد

        except User.DoesNotExist:
            messages.error(request, "نام کاربری یا ایمیل معتبر نیست")
            return redirect("forgot_password")

    return render(request, "Shop/forgot_password.html")


def verify_reset_code(request):
    if request.method == "POST":
        entered_code = request.POST.get("reset_code")  # بررسی وجود مقدار
        if entered_code and entered_code == request.session.get("reset_code"):
            try:
                user = User.objects.get(email=request.session.get("user_email"))
                login(request, user)  # ورود موفق
                
                messages.success(request, "با موفقیت وارد شدید!")
                
                # حذف اطلاعات نشست پس از ورود موفق
                del request.session['reset_code']
                del request.session['user_email']

                return redirect("index_shop")  # انتقال به صفحه اصلی
            except User.DoesNotExist:
                messages.error(request, "مشکلی در ورود به حساب وجود دارد.")
                return redirect("forgot_password")
        else:
            messages.error(request, "کد وارد شده نامعتبر است، لطفاً دوباره تلاش کنید.")
            return redirect("verify_reset")

    return render(request, "Shop/verify_reset_code.html")




def generate_verification_code():
    return str(random.randint(100000, 999999))  # تولید یک کد تصادفی ۶ رقمی

def signup_user(request):
    form = SignUpForm()

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            password1 = form.cleaned_data["password1"]
            email = form.cleaned_data["email"]
            user = authenticate(request, username=username, password=password1)
            verification_code = generate_verification_code()  # تولید کد تأیید
            request.session["verification_code"] = verification_code  # ذخیره کد در سشن
            request.session["user_email"] = email  # ذخیره ایمیل کاربر

            # ارسال ایمیل کد تأیید
            send_mail(
                subject="کد تأیید شما",
                message=f"سلام {username}! کد تأیید شما: {verification_code}",
                from_email="nejadimahan6@gmail.com",
                recipient_list=[email],
                fail_silently=False,
            )

            # ارسال ایمیل خوش‌آمدگویی
            send_mail(
                subject="خوش آمدید به سامانه ما!",
                message=f"سلام {username} عزیز!\n\nبه سامانه ما خوش آمدید. ما از حضور شما خوشحالیم و امیدواریم تجربه‌ای فوق‌العاده داشته باشید.\n\nبا آرزوی موفقیت برای شما!",
                from_email="nejadimahan6@gmail.com",
                recipient_list=[email],
                fail_silently=False,
            )

        return redirect("verifycation_code")  # ارسال کاربر به صفحه وارد کردن کد
    return render(request, "Shop/signup.html", {"form": form})


def logout_user(request):
    logout(request)
    messages.success(request, ("از اکانت با موفقیت خارج شدید"))
    return redirect("index_shop")

def verifycation_code(request):
        return render(request, "Shop/verifycation_code.html")
def verify_code(request):
    if request.method == "POST":
        entered_code = request.POST.get("verification_code")
        saved_code = request.session.get("verification_code")

        if entered_code == saved_code:
            messages.success(request, "کد تأیید صحیح است. حساب شما تأیید شد!")
            return redirect("index_shop")
        else:
            messages.error(request, "کد تأیید اشتباه است! لطفاً دوباره امتحان کنید.")
            return redirect("verifycation_code")

    return render(request, "verify_code.html")
def resend_code(request):
    if request.method == "POST":
        email = request.session.get("user_email")
        verification_code = generate_verification_code()
        request.session["verification_code"] = verification_code

        send_mail(
            subject="کد تأیید جدید شما",
            message=f"کد تأیید جدید شما: {verification_code}",
            from_email="nejadimahan6@gmail.com",
            recipient_list=[email],
            fail_silently=False,
        )

        messages.success(request, "کد جدید به ایمیل شما ارسال شد!")
        return redirect("verifycation_code")

