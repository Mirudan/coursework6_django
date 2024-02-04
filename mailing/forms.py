from django import forms

from clients.models import Client
from mailing.models import MailingMessage, MailingSettings


class StyleFormMixin:
    """Миксин для красивого отображения полей формы"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, forms.ChoiceField):
                field.widget.attrs['class'] = 'form-select'
            elif isinstance(field, forms.BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control mt-2 mb-2'


class MailingForm(StyleFormMixin, forms.ModelForm):
    """Основная форма создания рассылки: тема, сообщение, список получателей"""
    recipient = forms.ModelMultipleChoiceField(queryset=Client.objects.none(), widget=forms.SelectMultiple)

    class Meta:
        model = MailingMessage
        fields = ['subject', 'body', 'recipient', ]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        if user.is_superuser:
            self.fields['recipient'].queryset = Client.objects.all()
        else:
            self.fields['recipient'].queryset = Client.objects.filter(owner=user)


class MailingSettingsForm(StyleFormMixin, forms.ModelForm):
    """Дополнительная форма для рассылки: время начала, время окончания, периодичность"""

    class Meta:
        model = MailingSettings
        fields = ['mailing_start', 'mailing_end', 'mailing_period', 'next_sending_date']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['next_sending_date'].widget = forms.HiddenInput()


class ManagerMailingForm(StyleFormMixin, forms.ModelForm):
    """Форма для менеджера для отключения рассылок"""

    class Meta:
        model = MailingMessage
        fields = ('is_published',)

    def __init__(self, *args, **kwargs):
        kwargs.pop('user')
        super().__init__(*args, **kwargs)
