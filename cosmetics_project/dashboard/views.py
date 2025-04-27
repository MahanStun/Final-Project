from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import View
from django.contrib.auth.views import LoginView
from django.contrib import messages
from .models import UserProfile, Ticket, Blog
from .forms import UserProfileForm, BlogForm

class DashboardView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            messages.error(request, "لطفا اول وارد اکانت شوید")
            return redirect("login")  

        try:
            user_profile, _ = UserProfile.objects.get_or_create(user=request.user)
            tickets = Ticket.objects.filter(user=request.user)
            blogs = Blog.objects.all()  # دریافت لیست بلاگ‌ها
            form = UserProfileForm(instance=user_profile)
            form_blog = BlogForm()
            return render(request, "dashboard/dashboard.html", {
                "form": form, 
                "profile": user_profile, 
                "tickets": tickets, 
                "form_blog": form_blog, 
                "blogs": blogs  # ارسال لیست بلاگ‌ها به صفحه
            })
        except:
            messages.error(request, "مشکلی در بارگذاری داشبورد رخ داده است")
            return redirect("dashboard")


    def post(self, request):
        if not request.user.is_authenticated:
            return redirect("login")

        if "subject" in request.POST and "message" in request.POST:
            Ticket.objects.create(user=request.user, subject=request.POST["subject"], message=request.POST["message"])
            messages.success(request, "تیکت با موفقیت ثبت شد")
            return redirect("dashboard")

        user_profile, _ = UserProfile.objects.get_or_create(user=request.user)
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, "اطلاعات پروفایل با موفقیت ذخیره شد")
            return redirect("dashboard")

        return render(request, "dashboard/dashboard.html", {"form": form, "profile": user_profile})


def add_blog(request):
    if not request.user.is_authenticated:
        messages.error(request, "لطفا اول وارد اکانت شوید")
        return redirect("login")

    form_blog = BlogForm(request.POST or None, request.FILES or None)
    
    if request.method == 'POST':
        if form_blog.is_valid():
            try:
                blog = form_blog.save(commit=False)
                blog.author = request.user
                blog.save()
                messages.success(request, "بلاگ با موفقیت اضافه شد")
                return redirect("dashboard")
            except Exception as e:
                messages.error(request, f"خطا در ذخیره بلاگ: {e}")
        else:
            messages.error(request, "فرم معتبر نیست. لطفاً اطلاعات را بررسی کنید.")

    blogs = Blog.objects.all()  # ارسال لیست بلاگ‌ها به صفحه داشبورد
    print(form_blog.errors)
    print("Blog Author:", blog.author)

    return render(request, "dashboard/dashboard.html", {"form_blog": form_blog, "blogs": blogs})

from django.shortcuts import get_object_or_404

def delete_blog(request, blog_id):
    if not request.user.is_authenticated:
        messages.error(request, "لطفا اول وارد اکانت شوید")
        return redirect("login")

    blog = get_object_or_404(Blog, id=blog_id)

    if blog.author == request.user:  # فقط نویسنده بلاگ اجازه حذف دارد
        blog.delete()
        messages.success(request, "بلاگ با موفقیت حذف شد")
    else:
        messages.error(request, "شما اجازه حذف این بلاگ را ندارید")

    return redirect("dashboard")
