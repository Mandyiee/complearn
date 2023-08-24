from django.urls import path
from . import views


urlpatterns = [
    path("",  views.get_matrix, name="get_matrix"),
]
