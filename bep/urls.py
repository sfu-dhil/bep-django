from django.urls import path
from django.views.decorators.cache import cache_page
from django.conf import settings

from . import views
from .api import api

urlpatterns = [
    path("", views.HomeView.as_view(), name='home'),
    path("about/", views.AboutView.as_view(), name='about'),
    path("parishes/", views.ParishesView.as_view(), name='parishes'),
    path("parishes/<int:pk>/", views.ParisView.as_view(), name='parish'),
    path("transactions/", views.TransactionsView.as_view(), name='transactions'),
    # path("transactions/<int:pk>/", views.ParisView.as_view(), name='transaction'),
    path("api/", api.urls),
    path("api/geo/dioceses/pre1541/tiles/<int:z>/<int:x>/<int:y>", cache_page(settings.CACHE_SECONDS)(views.DiocesePre1541TileView.as_view()), name="diocese-pre1541-tiles"),
    path("api/geo/dioceses/post1541/tiles/<int:z>/<int:x>/<int:y>", cache_page(settings.CACHE_SECONDS)(views.DiocesePost1541TileView.as_view()), name="diocese-post1541-tiles"),
]