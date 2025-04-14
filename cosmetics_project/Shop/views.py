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
class UserEditView(generic.UpdateView):
    form_class = UserChangeForm
    template_name = "Shop/setting.html"
    success_url = reverse_lazy("index_blog")
    def get_object(self):
        return self.request.user



def index_shop(request):
        return render(request, "shop/index.html")

def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # EmailConfirmation(request, username, emailto,)
            messages.success(request, ("با موفقیت وارد اکانت شدید"))
            return redirect("index_blog")
        
        else:
            messages.error(request, ("ورود با خطا مواجه شده است"))
            return redirect("login_url")

    else:
        return render(request, "Shop/login.html")
def edit_user(request):
    pass





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
    return redirect("index_blog")
from django.shortcuts import render
from django.http import HttpResponse

from django.shortcuts import render
from django.http import HttpResponse

def quiz_view(request):
    if request.method == "POST":
        correct_answers = {
            "q1": "Arthur_Morgan",
            "q2": "HyperText"
        }
        user_answers = request.POST
        score = 0
        results = {}

        for question, correct_answer in correct_answers.items():
            user_answer = user_answers.get(question, "").strip()  # حذف فاصله‌های اضافی
            if user_answer.lower() == correct_answer.lower():  # تطبیق حساسیت به حروف کوچک و بزرگ
                results[question] = "✅ صحیح"
                score += 1
            else:
                results[question] = "❌ غلط"

        return render(request, "Shop/quiz_result.html", {"results": results, "score": score})

    return HttpResponse("لطفاً از طریق فرم اقدام کنید.")

def verifycation_code(request):
        return render(request, "Shop/verifycation_code.html")
def verify_code(request):
    if request.method == "POST":
        entered_code = request.POST.get("verification_code")
        saved_code = request.session.get("verification_code")

        if entered_code == saved_code:
            messages.success(request, "کد تأیید صحیح است. حساب شما تأیید شد!")
            return redirect("index_blog")
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

def exam(request):
        return render(request, "Shop/exam.html")
