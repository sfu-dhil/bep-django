from django.urls import path

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
    views.DiocesePre1541TileView.get_url(prefix='dioceses/tiles/pre1541', url_name="diocese-tiles-pre-1541"),
    views.DiocesePost1541TileView.get_url(prefix='dioceses/tiles/post1541', url_name="diocese-tiles-post-1541"),
]