from django import forms

from clients.models import Client


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


class ClientForm(StyleFormMixin, forms.ModelForm):
    """Форма для создания нового подписчика рассылки"""

    class Meta:
        model = Client
        exclude = ('owner',)
