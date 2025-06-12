from django.urls import path
from django.views.decorators.cache import cache_page
from django.conf import settings

from . import views
from .api import api

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("about/", views.AboutView.as_view(), name="about"),
    path("privacy/", views.PrivacyView.as_view(), name="privacy"),
    path("parishes/", views.ParishListView.as_view(), name="parish-list"),
    path("parishes/<int:pk>/", views.ParishDetailsView.as_view(), name="parish-details"),
    path("books/", views.BookListView.as_view(), name="book-list"),
    path("books/<int:pk>/", views.BookDetailsView.as_view(), name="book-details"),
    path("api/", api.urls),
    path("dioceses/tiles/pre1541/<int:z>/<int:x>/<int:y>", cache_page(settings.CACHE_SECONDS)(views.DiocesePre1541TileView.as_view()), name="book-details"),
    path("dioceses/tiles/post1541/<int:z>/<int:x>/<int:y>", cache_page(settings.CACHE_SECONDS)(views.DiocesePost1541TileView.as_view()), name="book-details"),
]