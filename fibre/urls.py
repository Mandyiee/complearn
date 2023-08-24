from django.urls import path
from . import views


urlpatterns = [
    path("",  views.get_fibre, name="get_fibre"),
]
