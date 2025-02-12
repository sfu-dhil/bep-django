from django.urls import path

from . import views
from .api import api

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("api/", api.urls),
]