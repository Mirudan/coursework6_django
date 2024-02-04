from django.urls import path

from clients.apps import ClientsConfig
from clients.views import *

app_name = ClientsConfig.name

urlpatterns = [
    path('view_all/', ClientListView.as_view(), name='all_clients'),
    path('create/', ClientCreateView.as_view(), name='add_client'),
    path('update/<int:pk>/', ClientUpdateView.as_view(), name='edit_client'),
    path('delete/<int:pk>/', ClientDeleteView.as_view(), name='delete_client'),
]
