from django.db.models.signals import post_save,post_delete,pre_delete,pre_save
from django.dispatch import receiver # decorator that get every signal
from django.core.mail import send_mail
from django.conf import settings
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.core.mail import send_mail

@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:  # یعنی کاربر تازه ثبت‌نام کرده
        subject = "خوش آمدید!"
        message = f"سلام {instance.username}! خوشحالیم که به ما پیوستی. 😊"
        from_email = "your_email@gmail.com"
        recipient_list = [instance.email]  # ایمیل کاربر ثبت‌نام شده

        send_mail(subject, message, from_email, recipient_list)