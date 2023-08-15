from celery import shared_task
from django.core.mail import send_mail
from social.models import Order

@shared_task
def order_confirmation_mail(order_id):
    """Task to send the order confirmation email

    Args:
        order_id (_type_): _description_
    """
    order = Order.objects.get(id=order_id)
    subject = f'Order nr. {order.id}'
    message = f'Dear {order.buyer.username},\n\n' \
              f'You have successfully placed an order.' \
              f'Your order ID is {order.id}.'
    mail_sent = send_mail(subject,
                          message,
                        'admin@myshop.com',
                        ["ravi.moolya28@gmail.com"])
    return mail_sent