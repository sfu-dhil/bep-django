from django.views.generic import TemplateView, DetailView, ListView
from django.db.models import F
from django.contrib.postgres.search import SearchHeadline, SearchQuery, SearchRank
from django.conf import settings
from vectortiles.views import MVTView

from .models import Parish, Book, Transaction
from .forms import TransactionSearchForm
from .schema import ParishSchema
from .vector_layers import DiocesePre1541VectorLayer, DiocesePre1541LabelVectorLayer, \
    DiocesePost1541VectorLayer, DiocesePost1541LabelVectorLayer

class HomeView(TemplateView):
    template_name = 'home.html'

class AboutView(TemplateView):
    template_name = 'about.html'

class ParishesView(ListView):
    paginate_by = 10
    model = Parish
    template_name = 'parishes.html'
    ordering = ['label']

    def get_queryset(self):
        queryset = super().get_queryset()

        q = self.request.GET.get('q')
        if q:
            query = SearchQuery(q, config='english', search_type='websearch')
            queryset = queryset \
                .filter(search_vector=query) \
                .annotate(rank=SearchRank(F('search_vector'), query) * 100) \
                .annotate(label_headline=SearchHeadline('label', query, start_sel='<mark>', stop_sel='</mark>', highlight_all=True)) \
                .annotate(description_headline=SearchHeadline('description', query, start_sel='<mark>', stop_sel='</mark>', min_words=3, max_words=10)) \
                .annotate(address_headline=SearchHeadline('address', query, start_sel='<mark>', stop_sel='</mark>', min_words=3, max_words=10)) \
                .order_by('-rank', 'label')

        return queryset

class ParisView(DetailView):
    model = Parish
    template_name = 'parish.html'

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

class TransactionsView(ListView):
    paginate_by = 10
    model = Transaction
    template_name = 'transactions.html'
    ordering = ['label']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = TransactionSearchForm()
        return context

    def get_queryset(self):
        queryset = Transaction.meilisearch
        search_str = ''

        form = TransactionSearchForm(self.request.GET)
        if form.is_valid():
            data = form.cleaned_data

            if data['value_min'] or data['value_max']:
                queryset = queryset.filter(value__range=(data['value_min'],data['value_max']))
            if data['shipping_min'] or data['shipping_max']:
                queryset = queryset.filter(shipping__range=(data['shipping_min'], data['shipping_max']))
            if data['year_min'] or data['year_max']:
                queryset = queryset.filter(year__range=(data['year_min'],data['year_max']))
            if data['monarch']:
                queryset = queryset.filter(monarch_id__exact=data['monarch'])
            if data['diocese']:
                queryset = queryset.filter(diocese_id__exact=data['diocese'])
            if data['county']:
                queryset = queryset.filter(county_id__exact=data['county'])
            if data['parish']:
                queryset = queryset.filter(parish_id__exact=data['parish'])
            if data['book']:
                queryset = queryset.filter(book_ids__exact=data['book'])
            if data['manuscript_source']:
                queryset = queryset.filter(manuscript_source_id__exact=data['manuscript_source'])
            if data['print_source']:
                queryset = queryset.filter(print_source_id__exact=data['print_source'])
            if data['injunction']:
                queryset = queryset.filter(injunction_id__exact=data['injunction'])

            if data['q']:
                search_str = data['q']

        return queryset.search(data['q'])

# class BookListView(ListView):
#     paginate_by = 10
#     model = Book
#     template_name = 'bookList.html'
#     ordering = ['title']

#     def get_queryset(self):
#         queryset = super().get_queryset()

#         q = self.request.GET.get('q')
#         if q:
#             query = SearchQuery(q, config='english', search_type='websearch')
#             queryset = queryset \
#                 .filter(search_vector=query) \
#                 .annotate(rank=SearchRank(F('search_vector'), query) * 100) \
#                 .annotate(title_headline=SearchHeadline('title', query, start_sel='<mark>', stop_sel='</mark>', highlight_all=True)) \
#                 .annotate(uniform_title_headline=SearchHeadline('uniform_title', query, start_sel='<mark>', stop_sel='</mark>', highlight_all=True)) \
#                 .annotate(author_headline=SearchHeadline('author', query, start_sel='<mark>', stop_sel='</mark>', highlight_all=True)) \
#                 .annotate(date_headline=SearchHeadline('date', query, start_sel='<mark>', stop_sel='</mark>', highlight_all=True)) \
#                 .annotate(imprint_headline=SearchHeadline('imprint', query, start_sel='<mark>', stop_sel='</mark>', min_words=3, max_words=10)) \
#                 .annotate(description_headline=SearchHeadline('description', query, start_sel='<mark>', stop_sel='</mark>', min_words=3, max_words=10)) \
#                 .order_by('-rank', 'title')

#         return queryset

# class BookDetailsView(DetailView):
#     model = Book
#     template_name = 'bookDetails.html'

class DiocesePre1541TileView(MVTView):
    layer_classes = [DiocesePre1541VectorLayer, DiocesePre1541LabelVectorLayer]

class DiocesePost1541TileView(MVTView):
    layer_classes = [DiocesePost1541VectorLayer, DiocesePost1541LabelVectorLayer]
