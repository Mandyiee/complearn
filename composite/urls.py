from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name=""),
     path("get_purpose", views.get_purpose, name="get_purpose"),
       path("make_composite", views.make_composite, name="make_composite"),
        path("composite/<uuid:id>", views.composite, name="composite"),
         path("error", views.error, name="composite-error"),
]
