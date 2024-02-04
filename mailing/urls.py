from django.urls import path

from mailing.apps import MailingConfig
from mailing.views import *

app_name = MailingConfig.name

urlpatterns = [
    path('create_mailing/', MailingCreateView.as_view(), name='create_mailing'),
    path('update/<int:pk>/', MailingUpdateView.as_view(), name='update_mailing'),
    path('delete/<int:pk>/', MailingDeleteView.as_view(), name='delete_mailing'),
    path('view_all/', MailingListView.as_view(), name='mailing_list'),
    path('view_details/<int:pk>/', MailingDetailView.as_view(), name='mailing_details'),
]
