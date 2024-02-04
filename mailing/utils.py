from django.core.mail import send_mail

import config.settings
from mailing.models import MailingMessage, MailingSettings


def get_mail_prepared(current_date):
    """
    Функция для подготовки рассылок
    :return: все опубликованные рассылки со статусом "запущена"
    """
    # получаем рассылки, у которых дата начала меньше и дата окончания больше текущей и статус "создана"
    new_mail = MailingMessage.objects.filter(is_published=True,
                                             setting__mailing_status=MailingSettings.STATUS.CREATED,
                                             setting__mailing_start__lte=current_date,
                                             setting__mailing_end__gte=current_date)

    # получаем рассылки, у которых дата окончания меньше текущей и статус "запущена"
    old_mail = MailingMessage.objects.filter(is_published=True,
                                             setting__mailing_status=MailingSettings.STATUS.RUNNING,
                                             setting__mailing_end__lt=current_date)

    # запускаем новые рассылки, у которых дата начала меньше и дата окончания больше текущей
    if new_mail.exists():
        for letter in new_mail:
            settings = letter.settings.filter(message_id=letter.pk)
            for setting in settings:
                setting.mailing_status = MailingSettings.STATUS.RUNNING
                setting.save()

    # завершаем рассылки, у которых дата окончания меньше текущей
    if old_mail.exists():
        for letter in old_mail:
            settings = letter.settings.filter(message_id=letter.pk)
            for setting in settings:
                setting.mailing_status = MailingSettings.STATUS.COMPLETED
                setting.save()

    # получаем все рассылки со статусом "запущена"
    running_mail = MailingMessage.objects.filter(is_published=True,
                                                 setting__mailing_status=MailingSettings.STATUS.RUNNING)

    return running_mail


def get_current_mail_for_sending_in_period(current_date, mail_queryset, frequency):
    current_mail_for_sending_in_period = mail_queryset.filter(setting__mailing_period=frequency,
                                                              setting__next_sending_date=current_date)

    return current_mail_for_sending_in_period


def send_ready_mail(all_mail):
    """
    Функция отправки писем каждому получателю в списке
    :param all_mail: queryset со списком получателей
    """
    for recipient in all_mail.recipient.all():
        send_mail(
            subject=all_mail.subject,
            message=all_mail.body,
            from_email=config.settings.EMAIL_HOST_USER,
            recipient_list=[recipient]
        )
