from django.views.generic import TemplateView, DetailView, ListView
from django.db.models import F, Q, CharField, Value
from django.contrib.postgres.search import SearchHeadline, SearchQuery, SearchRank
from vectortiles.views import MVTView
from django.db.models.functions import LPad, Cast
import json

from .models import Parish, Transaction, County, Diocese, Inventory
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
            .annotate(searchable_id=LPad(Cast('id', output_field=CharField()), 5, Value('0')))

        form = TransactionSearchForm(self.request.GET)
        if form.is_valid():
            data = form.cleaned_data

            if data.get('q'):
                query = SearchQuery(data.get('q'), config='english', search_type='websearch')
                queryset = queryset \
                    .filter(search_vector=query) \
                    .annotate(rank=SearchRank(F('search_vector'), query) * 100) \
                    .annotate(searchable_id_headline=SearchHeadline('searchable_id', query, start_sel='<mark>', stop_sel='</mark>', highlight_all=True)) \
                    .annotate(transcription_headline=SearchHeadline('transcription', query, start_sel='<mark>', stop_sel='</mark>', highlight_all=True)) \
                    .annotate(modern_transcription_headline=SearchHeadline('modern_transcription', query, start_sel='<mark>', stop_sel='</mark>', highlight_all=True)) \
                    .annotate(public_notes_headline=SearchHeadline('public_notes', query, start_sel='<mark>', stop_sel='</mark>', highlight_all=True)) \
                    .annotate(location_headline=SearchHeadline('location', query, start_sel='<mark>', stop_sel='</mark>', highlight_all=True)) \
                    .order_by('-rank', *self.get_ordering())

            if data.get('value_l_min') or data.get('value_s_min') or data.get('value_d_min'):
                queryset = queryset.filter(value__gte=Transaction.get_total_from_lsd(data.get('value_l_min'), data.get('value_s_min'), data.get('value_d_min')))
            if data.get('value_l_max') or data.get('value_s_max') or data.get('value_d_max'):
                queryset = queryset.filter(value__lte=Transaction.get_total_from_lsd(data.get('value_l_max'), data.get('value_s_max'), data.get('value_d_max')))
            if data.get('shipping_l_min') or data.get('shipping_s_min') or data.get('shipping_d_min'):
                queryset = queryset.filter(shipping__gte=Transaction.get_total_from_lsd(data.get('shipping_l_min'), data.get('shipping_s_min'), data.get('shipping_d_min')))
            if data.get('shipping_l_max') or data.get('shipping_s_max') or data.get('shipping_d_max'):
                queryset = queryset.filter(shipping__lte=Transaction.get_total_from_lsd(data.get('shipping_l_max'), data.get('shipping_s_max'), data.get('shipping_d_max')))
            if data.get('year_min'):
                queryset = queryset.filter(sort_year__gte=data.get('year_min'))
            if data.get('year_max'):
                queryset = queryset.filter(sort_year__lte=data.get('year_max'))
            if data.get('transaction_action'):
                queryset = queryset.filter(transaction_actions=data.get('transaction_action'))
            if data.get('transaction_medium'):
                queryset = queryset.filter(transaction_mediums=data.get('transaction_medium'))
            if data.get('monarch'):
                queryset = queryset.filter(monarch=data.get('monarch'))
            if data.get('diocese'):
                queryset = queryset.filter(parish__archdeaconry__diocese=data.get('diocese'))
            if data.get('county'):
                queryset = queryset.filter(parish__town__county=data.get('county'))
            if data.get('parish'):
                queryset = queryset.filter(parish=data.get('parish'))
            if data.get('book'):
                queryset = queryset.filter(books=data.get('book'))
            if data.get('manuscript_source'):
                queryset = queryset.filter(manuscript_source=data.get('manuscript_source'))
            if data.get('print_source'):
                queryset = queryset.filter(print_source=data.get('print_source'))
            if data.get('injunction'):
                queryset = queryset.filter(injunction=data.get('injunction'))

        return queryset

class TransactionView(DetailView):
    model = Transaction
    template_name = 'transaction.html'

    def get_queryset(self):
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = self.object.books.all()
        context['transaction_actions'] = self.object.transaction_actions.all()
        context['transaction_mediums'] = self.object.transaction_mediums.all()
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


class InventoryView(DetailView):
    model = Inventory
    template_name = 'inventory.html'

    def get_queryset(self):
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = self.object.books.all()
        context['manuscript_source'] = self.object.manuscript_source
        context['print_source'] = self.object.print_source
        context['monarch'] = self.object.monarch
        context['injunction'] = self.object.injunction
        context['inventory_images'] = self.object.images.all()

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
            .annotate(searchable_id=LPad(Cast('id', output_field=CharField()), 5, Value('0')))

        form = ParishSearchForm(self.request.GET)
        if form.is_valid():
            data = form.cleaned_data

            if data.get('q'):
                query = SearchQuery(data.get('q'), config='english', search_type='websearch')
                queryset = queryset \
                    .filter(search_vector=query) \
                    .annotate(rank=SearchRank(F('search_vector'), query) * 100) \
                    .annotate(label_headline=SearchHeadline('label', query, start_sel='<mark>', stop_sel='</mark>', highlight_all=True)) \
                    .annotate(description_headline=SearchHeadline('description', query, start_sel='<mark>', stop_sel='</mark>', highlight_all=True)) \
                    .annotate(address_headline=SearchHeadline('address', query, start_sel='<mark>', stop_sel='</mark>', highlight_all=True)) \
                    .order_by('-rank', *self.get_ordering())

            if data.get('diocese'):
                queryset = queryset.filter(archdeaconry__diocese=data.get('diocese'))
            if data.get('county'):
                queryset = queryset.filter(town__county=data.get('county'))

        return queryset

class ParisView(DetailView):
    model = Parish
    template_name = 'parish.html'

    def get_queryset(self):
        return super().get_queryset()

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
        context['visualization_parish_ids_json'] = json.dumps([self.object.pk])
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
            .annotate(searchable_id=LPad(Cast('id', output_field=CharField()), 5, Value('0')))

        form = DioceseSearchForm(self.request.GET)
        if form.is_valid():
            data = form.cleaned_data

            if data.get('q'):
                query = SearchQuery(data.get('q'), config='english', search_type='websearch')
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
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['province'] = self.object.province
        context['nation'] = context['province'].nation if context['province'] and context['province'].nation else None
        context['visualization_parish_ids_json'] = json.dumps(list(Parish.objects.filter(archdeaconry__diocese_id=self.object.pk).values_list('id', flat=True)))
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
            .annotate(searchable_id=LPad(Cast('id', output_field=CharField()), 5, Value('0')))

        form = CountySearchForm(self.request.GET)
        if form.is_valid():
            data = form.cleaned_data

            if data.get('q'):
                query = SearchQuery(data.get('q'), config='english', search_type='websearch')
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
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nation'] = self.object.nation
        context['visualization_parish_ids_json'] = json.dumps(list(Parish.objects.filter(town__county_id=self.object.pk).values_list('id', flat=True)))
        return context

class DiocesePre1541TileView(MVTView):
    layer_classes = [DiocesePre1541VectorLayer, DiocesePre1541LabelVectorLayer]

class DiocesePost1541TileView(MVTView):
    layer_classes = [DiocesePost1541VectorLayer, DiocesePost1541LabelVectorLayer]
