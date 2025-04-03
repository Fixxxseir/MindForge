from celery import shared_task
from django.core.mail import send_mass_mail

from config.settings import EMAIL_HOST_USER
from lms.models import Course, Subscription


@shared_task
def send_mail_course_update(course_id):
    """Отправляет уведомления об обновлении курса массово."""
    course = Course.objects.get(id=course_id)
    subscriptions = Subscription.objects.filter(course=course, is_active=True)
    if not subscriptions.exists():
        return

    emails = [s.user.email for s in subscriptions]
    subject = "У вас новое обновление!"
    message = f'Курс "{course.name}", на который вы подписаны, был обновлен.'

    email_messages = [(subject, message, EMAIL_HOST_USER, [email]) for email in
                      emails]
    send_mass_mail(email_messages)
