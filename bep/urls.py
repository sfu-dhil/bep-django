from django.urls import path
from django.views.decorators.cache import cache_page
from django.conf import settings

from . import views
from .api import api

urlpatterns = [
    path("", views.HomeView.as_view(), name='home'),
    path("about", views.AboutView.as_view(), name='about'),
    path("transactions", views.TransactionsView.as_view(), name='transactions'),
    path("transactions/<int:pk>", views.TransactionView.as_view(), name='transaction'),
    path("parishes", views.ParishesView.as_view(), name='parishes'),
    path("parishes/<int:pk>", views.ParisView.as_view(), name='parish'),
    path("dioceses", views.DiocesesView.as_view(), name='dioceses'),
    path("dioceses/<int:pk>", views.DioceseView.as_view(), name='diocese'),
    path("counties", views.CountiesView.as_view(), name='counties'),
    path("counties/<int:pk>", views.CountyView.as_view(), name='county'),
    path("api/", api.urls),
    path("api/geo/dioceses/pre1541/tiles/<int:z>/<int:x>/<int:y>", cache_page(settings.CACHE_SECONDS)(views.DiocesePre1541TileView.as_view()), name="diocese-pre1541-tiles"),
    path("api/geo/dioceses/post1541/tiles/<int:z>/<int:x>/<int:y>", cache_page(settings.CACHE_SECONDS)(views.DiocesePost1541TileView.as_view()), name="diocese-post1541-tiles"),
]