from django.views.generic import TemplateView, DetailView, ListView
from django.db.models import F, Q, CharField, Value
from django.contrib.postgres.search import SearchHeadline, SearchQuery, SearchRank
from vectortiles.views import MVTView
from django.db.models.functions import LPad, Cast

from .models import Parish, Transaction, County, Diocese
from .forms import TransactionSearchForm, ParishSearchForm, DioceseSearchForm, CountySearchForm
from .vector_layers import DiocesePre1541VectorLayer, DiocesePre1541LabelVectorLayer, \
    DiocesePost1541VectorLayer, DiocesePost1541LabelVectorLayer

class HomeView(TemplateView):
    template_name = 'home.html'

class AboutView(TemplateView):
    template_name = 'about.html'

class TransactionsView(ListView):
    paginate_by = 10
    model = Transaction
    template_name = 'transactions.html'
    ordering = ['id']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = TransactionSearchForm(self.request.GET)
        return context

    def get_queryset(self):
        queryset = super().get_queryset() \
            .annotate(searchable_id=LPad(Cast('id', output_field=CharField()), 5, Value('0'))) \
            .prefetch_related(
                'parish',
                'parish__town', 'parish__town__county', 'parish__town__county__nation',
                'parish__archdeaconry', 'parish__archdeaconry__diocese', 'parish__archdeaconry__diocese__province', 'parish__archdeaconry__diocese__province__nation',
                'manuscript_source', 'print_source', 'monarch', 'transaction_categories', 'books',
            )

        form = TransactionSearchForm(self.request.GET)
        if form.is_valid():
            data = form.cleaned_data

            if data['q']:
                query = SearchQuery(data['q'], config='english', search_type='websearch')
                queryset = queryset \
                    .filter(search_vector=query) \
                    .annotate(rank=SearchRank(F('search_vector'), query) * 100) \
                    .annotate(searchable_id_headline=SearchHeadline('searchable_id', query, start_sel='<mark>', stop_sel='</mark>', highlight_all=True)) \
                    .annotate(transcription_headline=SearchHeadline('transcription', query, start_sel='<mark>', stop_sel='</mark>', highlight_all=True)) \
                    .annotate(modern_transcription_headline=SearchHeadline('modern_transcription', query, start_sel='<mark>', stop_sel='</mark>', highlight_all=True)) \
                    .annotate(public_notes_headline=SearchHeadline('public_notes', query, start_sel='<mark>', stop_sel='</mark>', highlight_all=True)) \
                    .annotate(location_headline=SearchHeadline('location', query, start_sel='<mark>', stop_sel='</mark>', highlight_all=True)) \
                    .order_by('-rank', *self.get_ordering())

            if data['value_l_min'] or data['value_s_min'] or data['value_d_min']:
                queryset = queryset.filter(value__gte=Transaction.get_total_from_lsd(data['value_l_min'], data['value_s_min'], data['value_d_min']))
            if data['value_l_max'] or data['value_s_max'] or data['value_d_max']:
                queryset = queryset.filter(value__lte=Transaction.get_total_from_lsd(data['value_l_max'], data['value_s_max'], data['value_d_max']))
            if data['shipping_l_min'] or data['shipping_s_min'] or data['shipping_d_min']:
                queryset = queryset.filter(shipping__gte=Transaction.get_total_from_lsd(data['shipping_l_min'], data['shipping_s_min'], data['shipping_d_min']))
            if data['shipping_l_max'] or data['shipping_s_max'] or data['shipping_d_max']:
                queryset = queryset.filter(shipping__lte=Transaction.get_total_from_lsd(data['shipping_l_max'], data['shipping_s_max'], data['shipping_d_max']))
            if data['year_min']:
                queryset = queryset.filter(start_date__year__gte=data['year_min'])
            if data['year_max']:
                queryset = queryset.filter(start_date__year__lte=data['year_max'])
            if data['transaction_category']:
                queryset = queryset.filter(transaction_categories=data['transaction_category'])
            if data['monarch']:
                queryset = queryset.filter(monarch=data['monarch'])
            if data['diocese']:
                queryset = queryset.filter(parish__archdeaconry__diocese=data['diocese'])
            if data['county']:
                queryset = queryset.filter(parish__town__county=data['county'])
            if data['parish']:
                queryset = queryset.filter(parish=data['parish'])
            if data['book']:
                queryset = queryset.filter(books=data['book'])
            if data['manuscript_source']:
                queryset = queryset.filter(manuscript_source=data['manuscript_source'])
            if data['print_source']:
                queryset = queryset.filter(print_source=data['print_source'])
            if data['injunction']:
                queryset = queryset.filter(injunction=data['injunction'])

        return queryset

class TransactionView(DetailView):
    model = Transaction
    template_name = 'transaction.html'

    def get_queryset(self):
        return super().get_queryset() \
            .prefetch_related(
                'parish',
                'parish__town', 'parish__town__county', 'parish__town__county__nation',
                'parish__archdeaconry', 'parish__archdeaconry__diocese', 'parish__archdeaconry__diocese__province', 'parish__archdeaconry__diocese__province__nation',
                'manuscript_source', 'print_source', 'monarch', 'transaction_categories', 'books',
            )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = self.object.books.all()
        context['transaction_categories'] = self.object.transaction_categories.all()
        context['manuscript_source'] = self.object.manuscript_source
        context['print_source'] = self.object.print_source
        context['injunction'] = self.object.injunction
        context['monarch'] = self.object.monarch

        context['parish'] = self.object.parish
        context['town'] = context['parish'].town
        context['county'] = context['town'].county if context['town'] else None
        context['archdeaconry'] = context['parish'].archdeaconry
        context['diocese'] = context['archdeaconry'].diocese if context['archdeaconry'] else None
        context['province'] = context['diocese'].province if context['diocese'] else None
        if context['county'] and context['county'].nation:
            context['nation'] = context['county'].nation
        elif context['province'] and context['province'].nation:
            context['nation'] = context['province'].nation
        else:
            context['nation'] = None
        return context

class ParishesView(ListView):
    paginate_by = 10
    model = Parish
    template_name = 'parishes.html'
    ordering = ['label']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ParishSearchForm(self.request.GET)
        return context

    def get_queryset(self):
        queryset = super().get_queryset() \
            .annotate(searchable_id=LPad(Cast('id', output_field=CharField()), 5, Value('0'))) \
            .prefetch_related(
                'town', 'town__county', 'town__county__nation',
                'archdeaconry', 'archdeaconry__diocese', 'archdeaconry__diocese__province', 'archdeaconry__diocese__province__nation',
            )

        form = ParishSearchForm(self.request.GET)
        if form.is_valid():
            data = form.cleaned_data

            if data['q']:
                query = SearchQuery(data['q'], config='english', search_type='websearch')
                queryset = queryset \
                    .filter(search_vector=query) \
                    .annotate(rank=SearchRank(F('search_vector'), query) * 100) \
                    .annotate(label_headline=SearchHeadline('label', query, start_sel='<mark>', stop_sel='</mark>', highlight_all=True)) \
                    .annotate(description_headline=SearchHeadline('description', query, start_sel='<mark>', stop_sel='</mark>', highlight_all=True)) \
                    .annotate(address_headline=SearchHeadline('address', query, start_sel='<mark>', stop_sel='</mark>', highlight_all=True)) \
                    .order_by('-rank', *self.get_ordering())

            if data['diocese']:
                queryset = queryset.filter(archdeaconry__diocese=data['diocese'])
            if data['county']:
                queryset = queryset.filter(town__county=data['county'])

        return queryset

class ParisView(DetailView):
    model = Parish
    template_name = 'parish.html'

    def get_queryset(self):
        return super().get_queryset() \
            .prefetch_related(
                'town', 'town__county', 'town__county__nation',
                'archdeaconry', 'archdeaconry__diocese', 'archdeaconry__diocese__province', 'archdeaconry__diocese__province__nation',
            )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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

class DiocesesView(ListView):
    paginate_by = 10
    model = Diocese
    template_name = 'dioceses.html'
    ordering = ['label']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = DioceseSearchForm(self.request.GET)
        return context

    def get_queryset(self):
        queryset = super().get_queryset() \
            .annotate(searchable_id=LPad(Cast('id', output_field=CharField()), 5, Value('0'))) \
            .prefetch_related(
                'province', 'province__nation',
            )

        form = DioceseSearchForm(self.request.GET)
        if form.is_valid():
            data = form.cleaned_data

            if data['q']:
                query = SearchQuery(data['q'], config='english', search_type='websearch')
                queryset = queryset \
                    .filter(search_vector=query) \
                    .annotate(rank=SearchRank(F('search_vector'), query) * 100) \
                    .annotate(label_headline=SearchHeadline('label', query, start_sel='<mark>', stop_sel='</mark>', highlight_all=True)) \
                    .annotate(description_headline=SearchHeadline('description', query, start_sel='<mark>', stop_sel='</mark>', highlight_all=True)) \
                    .order_by('-rank', *self.get_ordering())

        return queryset

class DioceseView(DetailView):
    model = Diocese
    template_name = 'diocese.html'

    def get_queryset(self):
        return super().get_queryset() \
            .prefetch_related(
                'province', 'province__nation',
            )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['province'] = self.object.province
        context['nation'] = context['province'].nation if context['province'] and context['province'].nation else None
        return context

class CountiesView(ListView):
    paginate_by = 10
    model = County
    template_name = 'counties.html'
    ordering = ['label']


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CountySearchForm(self.request.GET)
        return context

    def get_queryset(self):
        queryset = super().get_queryset() \
            .annotate(searchable_id=LPad(Cast('id', output_field=CharField()), 5, Value('0'))) \
            .prefetch_related(
                'nation',
            )

        form = CountySearchForm(self.request.GET)
        if form.is_valid():
            data = form.cleaned_data

            if data['q']:
                query = SearchQuery(data['q'], config='english', search_type='websearch')
                queryset = queryset \
                    .filter(search_vector=query) \
                    .annotate(rank=SearchRank(F('search_vector'), query) * 100) \
                    .annotate(label_headline=SearchHeadline('label', query, start_sel='<mark>', stop_sel='</mark>', highlight_all=True)) \
                    .annotate(description_headline=SearchHeadline('description', query, start_sel='<mark>', stop_sel='</mark>', highlight_all=True)) \
                    .order_by('-rank', *self.get_ordering())

        return queryset

class CountyView(DetailView):
    model = County
    template_name = 'county.html'

    def get_queryset(self):
        return super().get_queryset() \
            .prefetch_related(
                'nation',
            )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nation'] = self.object.nation
        return context

class DiocesePre1541TileView(MVTView):
    layer_classes = [DiocesePre1541VectorLayer, DiocesePre1541LabelVectorLayer]

class DiocesePost1541TileView(MVTView):
    layer_classes = [DiocesePost1541VectorLayer, DiocesePost1541LabelVectorLayer]
