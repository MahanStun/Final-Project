from django.http import HttpResponse , HttpResponseBadRequest
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
from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import JsonResponse
from .models import Comment, Product
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import FormView
from dashboard.models import Product_dashboard , Category_dashboard ,Comment_dashboard

# Create your views here.


class UserEditView(generic.UpdateView):
    form_class = UserChangeForm
    template_name = "shop/setting.html"
    success_url = reverse_lazy("index_blog")
    def get_object(self):
        return self.request.user
def index_shop(request):
    Products = Product_dashboard.objects.all()
    categories = Category_dashboard.objects.all()  # دریافت همه دسته‌بندی‌ها
    if request.method == "POST":
        query = request.POST.get("search-course")
        if query:
            Products = Product_dashboard.objects.filter(Product_name__icontains=query)
    paginator = Paginator(Products,3)
    page_number = request.GET.get("page",1)
    page_obj = paginator.get_page(page_number)
    return render(request, "shop/index.html",{"Products": Products , "page_obj" : page_obj,"categories": categories})

    #return HttpResponse("welcome")
def Products_Cosmetics(request, pk):
    Productss = Product_dashboard.objects.get(id=pk)
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
            return redirect("index_blog")
        
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

                return redirect("index_blog")  # انتقال به صفحه اصلی
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
    return redirect("index_blog")

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
    

def category(request, cat=None):
    print(f"دسته‌بندی درخواست‌شده: {cat}")  # بررسی مقدار دریافتی
    
    if cat is not None:
        try:
            category = Category_dashboard.objects.get(slug=cat)  # بررسی دسته‌بندی
            print(f"دسته‌بندی پیدا شد: {category.name}")  
        except Category_dashboard.DoesNotExist:
            return render(request, "shop/errorPage.html", {"message": "دسته‌بندی پیدا نشد."})

        Products = Product_dashboard.objects.filter(category=category)
        print(f"تعداد محصولات یافت‌شده: {Products.count()}")  # نمایش تعداد محصولات

        return render(request, "shop/category.html", {"Products": Products, "category": category})





@login_required
def add_comment(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return JsonResponse({"error": "User not authenticated"}, status=401)

        content = request.POST.get('content')
        product_id = request.POST.get('product_id')
        if not product_id or not product_id.isdigit():
            return JsonResponse({"error": "Invalid product ID"}, status=400)

        try:
            product = Product_dashboard.objects.get(id=product_id)
            new_comment = Comment_dashboard.objects.create(
                content=content,
                product=product,
                user=request.user
            )
            return JsonResponse({'content': new_comment.content, 'user': request.user.username})
        except Product_dashboard.DoesNotExist:
            return JsonResponse({"error": "Product not found"}, status=404)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)

def get_comments(request):
    product_id = request.GET.get('product_id')
    if not product_id or not product_id.isdigit():
        return JsonResponse({"error": "Invalid product ID"}, status=400)
    
    try:
        product = Product_dashboard.objects.get(id=product_id)
        comments = Comment_dashboard.objects.filter(product=product).values('id', 'content', 'created_at', 'user__username', 'user_id')
        user_id = request.user.id
        comments_list = []

        for comment in comments:
            comments_list.append({
                "id": comment["id"],
                "content": comment["content"],
                "created_at": comment["created_at"],
                "user": "خودم" if user_id == comment["user_id"] else comment["user__username"],
                "is_owner": user_id == comment["user_id"],
            })

        return JsonResponse(comments_list, safe=False)
    except Product_dashboard.DoesNotExist:
        return JsonResponse({"error": "Product not found"}, status=404)

@login_required
def delete_comment(request):
    if request.method == 'POST':
        comment_id = request.POST.get('comment_id')

        if not comment_id or not comment_id.isdigit():
            return JsonResponse({"error": "Invalid comment ID"}, status=400)

        try:
            comment = Comment_dashboard.objects.get(id=comment_id, user=request.user)
            comment.delete()
            return JsonResponse({"success": "Comment deleted successfully"})
        except Comment_dashboard.DoesNotExist:
            return JsonResponse({"error": "Comment not found or not owned by user"}, status=404)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)

def check_comments(request):
    comments = Comment_dashboard.objects.all().values('id', 'content')
    return JsonResponse({"comments": list(comments)}, safe=False)




class PasswordssChangeView(FormView):
    template_name = "shop/Password_email_change.html"
    form_class = PasswordChangingForm
    success_url = reverse_lazy('password_success')




    def get_form_kwargs(self):
        # دریافت مقادیر پیش‌فرض فرم
        kwargs = super().get_form_kwargs()
        # ارسال کاربر به فرم برای پردازش
        kwargs['user'] = self.request.user
        return kwargs


    def form_valid(self, form):
        print("Form submitted successfully!")  # نمایش پیام در کنسول
        user = self.request.user
        user.set_password(form.cleaned_data.get('new_password'))
        user.save()
        return super().form_valid(form)



def password_success(request):
        return render(request, "shop/password_success.html", {})
