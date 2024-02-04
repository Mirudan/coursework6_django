from django.urls import path

from main.apps import MainConfig
from main.views import index

app_name = MainConfig.name

urlpatterns = [
    path('', index, name='index'),
]
