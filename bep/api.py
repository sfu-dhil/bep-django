import orjson
from ninja_extra import NinjaExtraAPI
from ninja_extra.pagination import paginate, PaginatedResponseSchema
from ninja.decorators import decorate_view
from ninja.renderers import BaseRenderer
from django.views.decorators.cache import cache_page
from django.conf import settings
from django.db.models import F

from .schema import *
from .models import Parish, Transaction, Inventory, Holding, \
    Book, Monarch, \
    Nation, County, Town, Province, Diocese, Archdeaconry

class ORJSONRenderer(BaseRenderer):
    media_type = "application/json"

    def render(self, request, data, *, response_status):
        return orjson.dumps(data)

api = NinjaExtraAPI(
    title='Books in English Parishes API',
    renderer=ORJSONRenderer()
)

@api.get("/monarchs", response=PaginatedResponseSchema[MonarchSchema], url_name='monarchs')
@paginate
@decorate_view(cache_page(settings.CACHE_SECONDS))
def monarchs(request):
    return Monarch.objects.order_by('start_date').all()

@api.get("/nations", response=PaginatedResponseSchema[NationSchema], url_name='nations')
@paginate
@decorate_view(cache_page(settings.CACHE_SECONDS))
def nations(request):
    return Nation.objects.order_by('label').all()

@api.get("provinces", response=PaginatedResponseSchema[ProvinceSchema], url_name='provinces')
@paginate
@decorate_view(cache_page(settings.CACHE_SECONDS))
def provinces(request):
    return Province.objects.order_by('label').all()

@api.get("/dioceses", response=PaginatedResponseSchema[DioceseSchema], url_name='dioceses')
@paginate
@decorate_view(cache_page(settings.CACHE_SECONDS))
def dioceses(request):
    return Diocese.objects.annotate(
        nation_id=F('province__nation_id'),
    ).order_by('label').all()

@api.get("/archdeaconries", response=PaginatedResponseSchema[ArchdeaconrySchema], url_name='archdeaconries')
@paginate
@decorate_view(cache_page(settings.CACHE_SECONDS))
def archdeaconries(request):
    return Archdeaconry.objects.annotate(
        nation_id=F('diocese__province__nation_id'),
        province_id=F('diocese__province_id'),
    ).order_by('label').all()

@api.get("/counties", response=PaginatedResponseSchema[CountySchema], url_name='counties')
@paginate
@decorate_view(cache_page(settings.CACHE_SECONDS))
def counties(request):
    return County.objects.order_by('label').all()

@api.get("/towns", response=PaginatedResponseSchema[TownSchema], url_name='towns')
@paginate
@decorate_view(cache_page(settings.CACHE_SECONDS))
def towns(request):
    return Town.objects.annotate(
        nation_id=F('county__nation_id'),
    ).order_by('label').all()

@api.get("/parishes", response=PaginatedResponseSchema[ParishSchema], url_name='parishes')
@paginate(page_size=500)
@decorate_view(cache_page(settings.CACHE_SECONDS))
def parishes(request):
    return Parish.objects.annotate(
        nation_id=F('archdeaconry__diocese__province__nation_id'),
        province_id=F('archdeaconry__diocese__province_id'),
        diocese_id=F('archdeaconry__diocese_id'),
        county_id=F('town__county_id'),
    ).order_by('label').all()

@api.get("/books/{book_id}/transactions", response=PaginatedResponseSchema[TransactionSchema], url_name='book-transactions')
@paginate
@decorate_view(cache_page(settings.CACHE_SECONDS))
def book_transactions(request, book_id: int):
    return Transaction.objects.prefetch_related(
        'books'
    ).filter(books__id=book_id).order_by('start_date').all()
@api.get("/parishes/{parish_id}/transactions", response=PaginatedResponseSchema[TransactionSchema], url_name='parish-transactions')
@paginate
@decorate_view(cache_page(settings.CACHE_SECONDS))
def parishes_transactions(request, parish_id: int):
    return Transaction.objects.prefetch_related(
        'books'
    ).filter(parish_id=parish_id).order_by('start_date').all()
@api.get("/transactions/{transaction_id}", response=TransactionSchema, url_name='transaction')
@decorate_view(cache_page(settings.CACHE_SECONDS))
def transaction(request, transaction_id: int):
    return Transaction.objects.prefetch_related(
        'books'
    ).get(pk=transaction_id)

@api.get("/books/{book_id}/inventories", response=PaginatedResponseSchema[InventorySchema], url_name='book-inventories')
@paginate
@decorate_view(cache_page(settings.CACHE_SECONDS))
def book_inventories(request, book_id: int):
    return Inventory.objects.prefetch_related(
        'books'
    ).filter(books__id=book_id).order_by('start_date').all()
@api.get("/parishes/{parish_id}/inventories", response=PaginatedResponseSchema[InventorySchema], url_name='parish-inventories')
@paginate
@decorate_view(cache_page(settings.CACHE_SECONDS))
def parishes_inventories(request, parish_id: int):
    return Inventory.objects.prefetch_related(
        'books'
    ).filter(parish_id=parish_id).order_by('start_date').all()
@api.get("/inventories/{inventory_id}", response=InventorySchema, url_name='inventory')
@decorate_view(cache_page(settings.CACHE_SECONDS))
def inventories(request, inventory_id: int):
    return Inventory.objects.prefetch_related(
        'books'
    ).get(pk=inventory_id)

@api.get("/books/{book_id}/holdings", response=PaginatedResponseSchema[HoldingSchema], url_name='book-holdings')
@paginate
@decorate_view(cache_page(settings.CACHE_SECONDS))
def book_holdings(request, book_id: int):
    return Holding.objects.prefetch_related(
        'books'
    ).filter(books__id=book_id).order_by('start_date').all()
@api.get("/parishes/{parish_id}/holdings", response=PaginatedResponseSchema[HoldingSchema], url_name='parish-holdings')
@paginate
@decorate_view(cache_page(settings.CACHE_SECONDS))
def parishes_holdings(request, parish_id: int):
    return Holding.objects.prefetch_related(
        'books'
    ).filter(parish_id=parish_id).order_by('start_date').all()
@api.get("/holdings/{holding_id}", response=HoldingSchema, url_name='holding')
@decorate_view(cache_page(settings.CACHE_SECONDS))
def holding(request, holding_id: int):
    return Holding.objects.prefetch_related(
        'books'
    ).get(pk=holding_id)

@api.get("/books", response=PaginatedResponseSchema[BookSchema], url_name='books')
@paginate
@decorate_view(cache_page(settings.CACHE_SECONDS))
def books(request):
    return Book.objects.order_by('title', 'date').all()
@api.get("/books/{book_id}", response=PaginatedResponseSchema[BookSchema], url_name='book')
@paginate
@decorate_view(cache_page(settings.CACHE_SECONDS))
def book(request, book_id: int):
    return Book.objects.get(pk=book_id)


@api.get("/geo/parishes", response=ParishFeatureCollectionGeoJsonSchema)
@decorate_view(cache_page(settings.CACHE_SECONDS))
def get_my_geojson(request):
    features = []
    parishes = Parish.objects.annotate(
        county_id=F('town__county_id'),
        # nation_id=F('archdeaconry__diocese__province__nation_id'),
        # province_id=F('archdeaconry__diocese__province_id'),
        # diocese_id=F('archdeaconry__diocese_id'),
    ).filter(geom_point__isnull=False).all()
    for parish in parishes:
        feature = ParishFeatureGeoJsonSchema(
            id=parish.pk,
            geometry=PointGeometrySchema(coordinates=parish.geom_point.coords),
            properties=ParishFeaturePropertiesSchema(
                label=parish.label,
                county_id=parish.county_id,
                # nation_id=parish.nation_id,
                # province_id=parish.province_id,
                # diocese_id=parish.diocese_id,
                # archdeaconry_id=parish.archdeaconry_id,
            )
        )
        features.append(feature)
    return ParishFeatureCollectionGeoJsonSchema(features=features)