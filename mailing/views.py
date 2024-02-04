from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.forms import inlineformset_factory
from django.http import HttpResponseForbidden
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from mailing.forms import MailingForm, ManagerMailingForm, MailingSettingsForm
from mailing.models import MailingMessage, MailingSettings


class GetUserForFormMixin:
    def get_form_kwargs(self):
        """Метод для получения конкретного пользователя для передачи в форму,
        чтобы вывести в форме список клиентов только этого пользователя"""
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class MailingListView(LoginRequiredMixin, ListView):
    """Представление для вывода списка всех рассылок"""
    paginate_by = 50
    model = MailingMessage
    template_name = 'mailing/mailing_list.html'
    extra_context = {'title': 'Список рассылок'}

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.has_perm('mailing.view_mailingmessage'):
            return queryset.order_by('pk')
        else:
            return queryset.filter(owner=self.request.user).order_by('-pk')


class MailingDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    """Представление для просмотра одной рассылки"""
    model = MailingMessage
    template_name = 'mailing/mailing_details.html'
    permission_required = 'mailing.view_mailingmessage'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['settings'] = MailingSettings.objects.filter(message_id=self.kwargs.get('pk'))
        return context

    def has_permission(self):
        obj = self.get_object()
        return obj.owner == self.request.user or super().has_permission()

    def handle_no_permission(self):
        return HttpResponseForbidden("У вас нет прав для просмотра этого объекта.")


class MailingCreateView(LoginRequiredMixin, GetUserForFormMixin, CreateView):
    """Представление для создания рассылки"""
    model = MailingMessage
    template_name = 'mailing/mailing_form.html'
    form_class = MailingForm
    success_url = reverse_lazy('mailing:mailing_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создание рассылки'
        formset_factory = inlineformset_factory(MailingMessage, MailingSettings, form=MailingSettingsForm,
                                                extra=1, can_delete=False)
        if self.request.method == 'POST':
            context['formset'] = formset_factory(self.request.POST, )
            # queryset=MailingMessage.objects.filter(recipient=self.request.user))
        else:
            context['formset'] = formset_factory()

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']

        if form.is_valid() and formset.is_valid():
            self.object = form.save()
            self.object.owner = self.request.user
            self.object.save()

            formset.instance = self.object
            for f in formset:
                date_start = f.cleaned_data.get('mailing_start')
                date_end = f.cleaned_data.get('mailing_end')
                if date_start is not None:
                    if date_start < datetime.now().date():
                        form.add_error(None, "Рассылка не должна начинаться задним числом")
                        return self.form_invalid(form=form)
                    elif date_start > date_end:
                        form.add_error(None, "Дата начала рассылки должна быть меньше даты окончания")
                        return self.form_invalid(form=form)
            formset.save()
            return super().form_valid(form)
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context)


class MailingUpdateView(LoginRequiredMixin, UserPassesTestMixin, GetUserForFormMixin, UpdateView):
    """Представление для редактирования рассылки"""
    model = MailingMessage
    template_name = 'mailing/mailing_form.html'
    form_class = MailingForm
    success_url = reverse_lazy('mailing:mailing_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактирование рассылки'
        if self.request.user == self.object.owner or self.request.user.is_superuser:
            formset_factory = inlineformset_factory(MailingMessage, MailingSettings, form=MailingSettingsForm,
                                                    extra=1, can_delete=True)
            if self.request.method == 'POST':
                context['formset'] = formset_factory(self.request.POST, instance=self.object)
            else:
                context['formset'] = formset_factory(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            for f in formset:
                if f.instance.mailing_start is not None:
                    f.instance.next_sending_date = f.instance.mailing_start
            formset.save()
            return super().form_valid(form)
        else:
            return self.form_invalid(form)

    def test_func(self):
        obj = self.get_object()
        return (obj.owner == self.request.user
                or self.request.user.has_perms(['mailing.can_cancel_mailing'])
                or self.request.user.is_superuser)

    def get_form_class(self):
        if (self.request.user.has_perm('mailing.can_cancel_mailing') and not self.request.user.is_superuser
                and not self.request.user == self.object.owner):
            return ManagerMailingForm
        return MailingForm

    def form_invalid(self, form):
        pass


class MailingDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Представление для удаления рассылки"""
    model = MailingMessage
    template_name = 'mailing/mailing_delete.html'
    success_url = reverse_lazy('mailing:mailing_list')

    def test_func(self):
        obj = self.get_object()
        return self.request.user.is_superuser or obj.owner == self.request.user
