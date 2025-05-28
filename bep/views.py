from functools import reduce
from operator import or_
from hashlib import md5
import re

from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView, DetailView, ListView
from django.db.models import F
from django.contrib.postgres.search import SearchHeadline, SearchQuery, SearchRank
from django.conf import settings
from vectortiles.views import MVTView

from .models import Parish, Book
from .schema import ParishSchema
from .vector_layers import DiocesePre1541VL, DiocesePost1541VL

class HomeView(TemplateView):
    template_name = 'home.html'

class AboutView(TemplateView):
    template_name = 'about.html'

class PrivacyView(TemplateView):
    template_name = 'privacy.html'

class ParishListView(ListView):
    paginate_by = 10
    model = Parish
    template_name = 'parishList.html'

    def get_queryset(self):
        q = self.request.GET.get('q')
        if q:
            query = reduce(or_, [SearchQuery(word, config='english') for word in re.split(r'\s+', q)])
            return Parish.objects \
                .filter(search_vector=query) \
                .annotate(rank=SearchRank(F('search_vector'), query) * 100) \
                .annotate(label_headline=SearchHeadline('label', query, start_sel='<mark>', stop_sel='</mark>', highlight_all=True)) \
                .annotate(description_headline=SearchHeadline('description', query, start_sel='<mark>', stop_sel='</mark>', min_words=3, max_words=10)) \
                .annotate(address_headline=SearchHeadline('address', query, start_sel='<mark>', stop_sel='</mark>', min_words=3, max_words=10)) \
                .order_by('-rank', 'label')
        else:
            return Parish.objects.order_by('label').all()

class ParishDetailsView(DetailView):
    model = Parish
    template_name = 'parishDetails.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['parish_data'] = ParishSchema.from_orm(self.object).dict()
        context['town'] = self.object.town
        context['county'] = context['town'].county if context['town'] else None
        context['archdeaconry'] = self.object.archdeaconry
        context['diocese'] = context['archdeaconry'].diocese if context['archdeaconry'] else None
        context['province'] = context['diocese'].province if context['diocese'] else None
        if context['county'] and context['county'].nation:
            context['nation'] = context['county'].nation
        elif context['province'] and context['province'].nation:
            context['nation'] = context['province'].nation
        else:
            context['nation'] = None
        return context


class BookListView(ListView):
    paginate_by = 10
    model = Book
    template_name = 'bookList.html'

    def get_queryset(self):
        q = self.request.GET.get('q')
        if q:
            query = reduce(or_, [SearchQuery(word, config='english') for word in re.split(r'\s+', q)])
            return Book.objects \
                .filter(search_vector=query) \
                .annotate(rank=SearchRank(F('search_vector'), query) * 100) \
                .annotate(title_headline=SearchHeadline('title', query, start_sel='<mark>', stop_sel='</mark>', highlight_all=True)) \
                .annotate(uniform_title_headline=SearchHeadline('uniform_title', query, start_sel='<mark>', stop_sel='</mark>', highlight_all=True)) \
                .annotate(author_headline=SearchHeadline('author', query, start_sel='<mark>', stop_sel='</mark>', highlight_all=True)) \
                .annotate(date_headline=SearchHeadline('date', query, start_sel='<mark>', stop_sel='</mark>', highlight_all=True)) \
                .annotate(imprint_headline=SearchHeadline('imprint', query, start_sel='<mark>', stop_sel='</mark>', min_words=3, max_words=10)) \
                .annotate(description_headline=SearchHeadline('description', query, start_sel='<mark>', stop_sel='</mark>', min_words=3, max_words=10)) \
                .order_by('-rank', 'title')
        else:
            return Book.objects.order_by('title').all()

class BookDetailsView(DetailView):
    model = Book
    template_name = 'bookDetails.html'

class DiocesePre1541TileView(MVTView):
    layer_classes = [DiocesePre1541VL]

    def get_tile(self, x, y, z):
        cache_key = md5(f"{self.get_id()}-{z}-{x}-{y}".encode()).hexdigest()
        if cache.has_key(cache_key):
            return cache.get(cache_key)
        tile = super().get_tile(x, y, z)
        cache.set(cache_key, tile, timeout=settings.CACHE_SECONDS) # timeout of 1 day
        return tile

class DiocesePost1541TileView(MVTView):
    layer_classes = [DiocesePost1541VL]

    def get_tile(self, x, y, z):
        cache_key = md5(f"{self.get_id()}-{z}-{x}-{y}".encode()).hexdigest()
        if cache.has_key(cache_key):
            return cache.get(cache_key)
        tile = super().get_tile(x, y, z)
        cache.set(cache_key, tile, timeout=settings.CACHE_SECONDS) # timeout of 1 day
        return tile
