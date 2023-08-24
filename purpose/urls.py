from django.urls import path
from . import views
urlpatterns = [
    path('',views.add_purpose,name='add-purpose')
]
