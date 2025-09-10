from django.urls import path
from main.views import show_index


urlpatterns = [
    path('', show_index, name='index'),
]
