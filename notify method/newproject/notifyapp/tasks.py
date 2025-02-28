from celery import shared_task
import datetime
from bson.objectid import ObjectId
from django.core.mail import send_mail
from django.conf import settings
from newproject.celery import app
from .models import Admin, Subscribtion, Notification

# @shared_task
# def send_expiry_notifications():
#     """
#     Send notification emails for expiring subscriptions.
#     """
#     today = datetime.date.today()
#     NOTIFICATION_MESSAGE = {
#         7: 'Your Premium Subscription Plan Will Expire In 7 Days',
#         5: 'Your Premium Subscription Plan Will Expire In 5 Days.',
#         1: 'Your Premium Subscription Plan Will Expire tomorrow.',
#         0: 'Your Premium Subscription Plan Expired!',
#     }

#     for days_left in [7, 5, 1, 0]:
#         target_date = today + datetime.timedelta(days=days_left) if days_left != 0 else today
#         expiring_subscriptions = Subscribtion.objects(expirey_date=target_date)

#         for subscribe in expiring_subscriptions:
#             admin = Admin.objects(admin_id=subscribe.admin_id).first()
#             if not admin:
#                 continue  

#             email = admin.email
#             message = NOTIFICATION_MESSAGE[days_left]
#             subject = 'Subscription Expire Notice'

#             send_mail(subject, message, settings.EMAIL_HOST_USER, [email], fail_silently=False)

#             Notification(
#                 notification_id=str(ObjectId()),
#                 admin_id=subscribe.admin_id,
#                 plan_type=subscribe.plan_name,
#                 message=message,
#                 sent_time=datetime.datetime.utcnow(),
#             ).save()

#     return "Notifications Sent!"
# myapp/tasks.py
# from celery import shared_task
# from django.core.mail import send_mail
from django.utils.timezone import now
from datetime import timedelta
# from myapp.models import SubscriptionPlan, Notification
# @app.task
@shared_task
def send_expiry_notifications():
    today = now().date()
    notifications_sent = []

    subscriptions = Subscribtion.objects.filter(is_active=True)
    for sub in subscriptions:
        if sub.create_date:
            expire_date = sub.create_date + timedelta(days=sub.duration_date)
            admin = Admin.objects(admin_id=sub.admin_id).first()
            if not admin:
                continue


            notification_dates = {
                "7 days before expiry": expire_date - timedelta(days=7),
                "5 days before expiry": expire_date - timedelta(days=5),
                "1 day before expiry": expire_date - timedelta(days=1),
                "Expired Today": expire_date,
                "Already expired for two days": expire_date + timedelta(days=2),
            }

            for msg, notify_date in notification_dates.items():
                if notify_date == today:
                    message = f"Dear {admin.email}, your subscription for {sub.plan_name} is {msg}."
                    print(f"🚀 Sending Notification: {message}")
                    notification_data = Notification(
                        admin_id=admin.admin_id,
                        plan_type="Subscription Alert",
                        message=message
                    )
                    notification_data.save()

                    send_mail(
                        subject="Subscription Expiry Notification",
                        message=message,
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=[admin.email],
                        fail_silently=False,
                    )

                    notifications_sent.append({"admin": admin.email, "message": message})

    return {"message": "Notifications sent successfully", "data": notifications_sent}