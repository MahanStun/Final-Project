from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import View
from django.contrib.auth.views import LoginView
from django.contrib import messages
from .models import UserProfile, Ticket, Blog , Category_dashboard, Product_dashboard
from .forms import UserProfileForm, BlogForm, UserChangeForm, ProductDashboardForm , CategoryForm
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User     
from django.utils.timezone import now, timedelta
from django.contrib.auth.models import User  # استفاده از مدل پیش‌فرض User



class DashboardView(View):
    def get(self, request):
            if not request.user.is_authenticated:
                messages.error(request, "لطفا اول وارد اکانت شوید")
                return redirect("login")  

            try:
                one_day_ago = now() - timedelta(days=1)
                active_users_count = User.objects.filter(last_login__gte=one_day_ago).count()

                user_profile, _ = UserProfile.objects.get_or_create(user=request.user)
                tickets = Ticket.objects.filter(user=request.user)
                blogs = Blog.objects.all()
                form = UserProfileForm(instance=user_profile)
                form_blog = BlogForm()
                category_form = CategoryForm()
                categories = Category_dashboard.objects.all()
                product_form = ProductDashboardForm()
                products = Product_dashboard.objects.all()
                all_users = User.objects.all()
                
                context = {
                    "form": form, 
                    "profile": user_profile, 
                    "tickets": tickets, 
                    "form_blog": form_blog, 
                    "blogs": blogs, 
                    "active_users": active_users_count,
                    "all_users": all_users,
                    "category_form": category_form,
                    "categories": categories,
                    "product_form": product_form,
                    "products": products,
                }
                return render(request, "dashboard/dashboard.html", context)
            except Exception as e:
                messages.error(request, f"مشکلی در بارگذاری داشبورد رخ داده است: {e}")
                return redirect("login_url")  # تغییر از "dashboard" به "login"

  

    def post(self, request):
        if not request.user.is_authenticated:
            return redirect("login")
        
        user = request.user
        form = UserChangeForm(request.POST, instance=user)

        if form.is_valid():
            form.save()  # ذخیره تغییرات کاربر
            messages.success(request, "اطلاعات کاربری با موفقیت تغییر کرد!")
            return redirect("dashboard")
        else:
            messages.error(request, "مشکلی در فرم وجود دارد. لطفا اطلاعات خود را بررسی کنید.")
            print(form.errors)  # نمایش خطاهای فرم برای دیباگ

        return render(request, "dashboard/dashboard.html", {"form": form})


def add_blog(request):
    if not request.user.is_authenticated:
        messages.error(request, "لطفا اول وارد اکانت شوید")
        return redirect("login_url")

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





def add_product_dash(request):
    if not request.user.is_authenticated:
        messages.error(request, "لطفا اول وارد اکانت شوید")
        return redirect("login")

    if request.method == 'POST':
        form = ProductDashboardForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "محصول با موفقیت اضافه شد")
            except Exception as e:
                messages.error(request, f"خطا در ذخیره محصول: {e}")
        else:
            messages.error(request, "فرم معتبر نیست. لطفاً اطلاعات را بررسی کنید.")
    
    return redirect("dashboard")

def delete_product_dash(request, product_id):
    if not request.user.is_authenticated:
        messages.error(request, "لطفا اول وارد اکانت شوید")
        return redirect("login")

    try:
        product = get_object_or_404(Product_dashboard, id=product_id)
        product.delete()
        messages.success(request, "محصول با موفقیت حذف شد")
    except Exception as e:
        messages.error(request, f"خطا در حذف محصول: {e}")
    
    return redirect("dashboard")

# در کلاس DashboardView، به متد get این موارد رو اضافه کنید:





def add_category(request):
    if not request.user.is_authenticated:
        messages.error(request, "لطفا اول وارد اکانت شوید")
        return redirect("login")

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            try:
                category = form.save(commit=False)
                if not category.slug:  # اگر مقدار slug وارد نشده باشد
                    category.slug = category.name.replace(' ', '-').lower()
                category.save()
                messages.success(request, "دسته‌بندی با موفقیت اضافه شد")
            except Exception as e:
                messages.error(request, f"خطا در ذخیره دسته‌بندی: {e}")
        else:
            messages.error(request, "فرم معتبر نیست. لطفاً اطلاعات را بررسی کنید.")
    
    return redirect("dashboard")


def delete_category(request, category_id):
        if not request.user.is_authenticated:
            messages.error(request, "لطفا اول وارد اکانت شوید")
            return redirect("login")

        try:
            category = get_object_or_404(Category_dashboard, id=category_id)
            category.delete()
            messages.success(request, "دسته‌بندی با موفقیت حذف شد")
        except Exception as e:
            messages.error(request, f"خطا در حذف دسته‌بندی: {e}")
        
        return redirect("dashboard")
