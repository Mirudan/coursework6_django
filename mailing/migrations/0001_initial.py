# Generated by Django 4.2.7 on 2024-02-04 11:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MailingLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(blank=True, choices=[('Успешно', 'Success'), ('Неуспешно', 'Failed')], max_length=9, null=True, verbose_name='статус отправки')),
                ('message', models.TextField(blank=True, null=True, verbose_name='ответ сервера')),
                ('date', models.DateTimeField(blank=True, null=True, verbose_name='время попытки')),
            ],
            options={
                'verbose_name': 'лог',
                'verbose_name_plural': 'логи',
                'ordering': ('status',),
            },
        ),
        migrations.CreateModel(
            name='MailingMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=150, verbose_name='тема письма')),
                ('body', models.TextField(blank=True, null=True, verbose_name='тело письма')),
                ('is_published', models.BooleanField(default=True, verbose_name='опубликована')),
            ],
            options={
                'verbose_name': 'рассылка',
                'verbose_name_plural': 'рассылки',
                'ordering': ('owner', 'is_published'),
                'permissions': [('can_cancel_mailing', 'Может отменять публикацию рассылки')],
            },
        ),
        migrations.CreateModel(
            name='MailingSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mailing_start', models.DateField(blank=True, null=True, verbose_name='начало рассылки')),
                ('mailing_end', models.DateField(blank=True, null=True, verbose_name='конец рассылки')),
                ('mailing_period', models.CharField(blank=True, choices=[('daily', 'Ежедневно'), ('weekly', 'Еженедельно'), ('monthly', 'Ежемесячно')], max_length=12, null=True, verbose_name='периодичность')),
                ('mailing_status', models.CharField(choices=[('created', 'Создана'), ('running', 'Запущена'), ('completed', 'Завершена')], default='created', max_length=10, verbose_name='статус рассылки')),
                ('next_sending_date', models.DateField(blank=True, null=True, verbose_name='следующая отправка')),
                ('message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='settings', related_query_name='setting', to='mailing.mailingmessage', verbose_name='рассылка')),
            ],
            options={
                'verbose_name': 'настройки рассылки',
                'verbose_name_plural': 'настройки рассылки',
                'ordering': ('mailing_start', 'mailing_end'),
            },
        ),
    ]
