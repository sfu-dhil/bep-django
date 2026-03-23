import orjson
from ninja_extra import NinjaExtraAPI
from ninja_extra.pagination import paginate, PaginatedResponseSchema
from ninja.renderers import BaseRenderer
from ninja.decorators import decorate_view
from django.views.decorators.cache import cache_page
from django.conf import settings
from django.db.models import F

from .schema import *
from .models import Parish, Transaction, Inventory, Holding, Injunction, \
    Book, Monarch, \
    Nation, County, Town, Province, Diocese, Archdeaconry, \
    TransactionCategory, PrintSource, ManuscriptSource, SourceCategory, Archive

class ORJSONRenderer(BaseRenderer):
    media_type = "application/json"

    def render(self, request, data, *, response_status):
        return orjson.dumps(data)

api = NinjaExtraAPI(
    title='Books in English Parishes API',
    renderer=ORJSONRenderer()
)



@api.get("/monarchs/{pk}", response=MonarchSchema)
@decorate_view(cache_page(settings.CACHE_SECONDS))
def monarch(request, pk: int):
    return Monarch.objects.prefetch_related('books').get(pk=pk)
@api.get("/monarchs", response=PaginatedResponseSchema[MonarchSchema])
@decorate_view(cache_page(settings.CACHE_SECONDS))
@paginate
def monarchs(request):
    return Monarch.objects.prefetch_related('books').order_by('start_date').all()



@api.get("/transaction/categories/{pk}", response=TransactionCategorySchema)
@decorate_view(cache_page(settings.CACHE_SECONDS))
def transaction_category(request, pk: int):
    return TransactionCategory.objects.get(pk=pk)
@api.get("/transaction/categories", response=PaginatedResponseSchema[TransactionCategorySchema])
@decorate_view(cache_page(settings.CACHE_SECONDS))
@paginate
def transaction_categories(request):
    return TransactionCategory.objects.order_by('label').all()



@api.get("/archives/{pk}", response=ArchiveSchema)
@decorate_view(cache_page(settings.CACHE_SECONDS))
def archive(request, pk: int):
    return Archive.objects.get(pk=pk)
@api.get("archives", response=PaginatedResponseSchema[ArchiveSchema])
@decorate_view(cache_page(settings.CACHE_SECONDS))
@paginate
def archives(request):
    return Archive.objects.order_by('label').all()



@api.get("/print/sources/{pk}", response=PrintSourceSchema)
@decorate_view(cache_page(settings.CACHE_SECONDS))
def print_source(request, pk: int):
    return PrintSource.objects.prefetch_related('source_category').get(pk=pk)
@api.get("/print/sources", response=PaginatedResponseSchema[PrintSourceSchema])
@decorate_view(cache_page(settings.CACHE_SECONDS))
@paginate
def print_sources(request):
    return PrintSource.objects.prefetch_related('source_category').order_by('title').all()



@api.get("/manuscript/sources/{pk}", response=ManuscriptSourceSchema)
@decorate_view(cache_page(settings.CACHE_SECONDS))
def manuscript_source(request, pk: int):
    return ManuscriptSource.objects.prefetch_related('archive', 'source_category').get(pk=pk)
@api.get("/manuscript/sources", response=PaginatedResponseSchema[ManuscriptSourceSchema])
@decorate_view(cache_page(settings.CACHE_SECONDS))
@paginate
def manuscript_sources(request):
    return ManuscriptSource.objects.prefetch_related('archive', 'source_category').order_by('label').all()



@api.get("/source/categories/{pk}", response=SourceCategorySchema)
@decorate_view(cache_page(settings.CACHE_SECONDS))
def source_category(request, pk: int):
    return SourceCategory.objects.prefetch_related('manuscript_sources', 'print_sources').get(pk=pk)
@api.get("/source/categories", response=PaginatedResponseSchema[SourceCategorySchema])
@decorate_view(cache_page(settings.CACHE_SECONDS))
@paginate
def source_categories(request):
    return SourceCategory.objects.prefetch_related('manuscript_sources', 'print_sources').order_by('label').all()



@api.get("/injunctions/{pk}", response=InjunctionSchema)
@decorate_view(cache_page(settings.CACHE_SECONDS))
def injunction(request, pk: int):
    return Injunction.objects.prefetch_related('monarch', 'archdeaconry', 'diocese', 'province', 'nation').get(pk=pk)
@api.get("/injunctions", response=PaginatedResponseSchema[InjunctionSchema])
@decorate_view(cache_page(settings.CACHE_SECONDS))
@paginate
def injunctions(request):
    return Injunction.objects.prefetch_related('monarch', 'archdeaconry', 'diocese', 'province', 'nation').order_by('title').all()



@api.get("/books/{pk}", response=BookSchema)
@decorate_view(cache_page(settings.CACHE_SECONDS))
def book(request, pk: int):
    return Book.objects.prefetch_related('monarch').get(pk=pk)
@api.get("/books", response=PaginatedResponseSchema[BookSchema])
@decorate_view(cache_page(settings.CACHE_SECONDS))
@paginate
def books(request):
    return Book.objects.prefetch_related('monarch').order_by('uniform_title').all()



@api.get("/nations/{pk}", response=NationSchema)
@decorate_view(cache_page(settings.CACHE_SECONDS))
def nation(request, pk: int):
    return Nation.objects.prefetch_related('provinces', 'counties', 'injunctions').get(pk=pk)
@api.get("/nations", response=PaginatedResponseSchema[NationSchema])
@decorate_view(cache_page(settings.CACHE_SECONDS))
@paginate
def nations(request):
    return Nation.objects.prefetch_related('provinces', 'counties', 'injunctions').order_by('label').all()


@api.get("provinces/{pk}", response=ProvinceSchema)
@decorate_view(cache_page(settings.CACHE_SECONDS))
def province(request, pk: int):
    return Province.objects.prefetch_related('nation', 'dioceses', 'injunctions').get(pk=pk)
@api.get("provinces", response=PaginatedResponseSchema[ProvinceSchema])
@decorate_view(cache_page(settings.CACHE_SECONDS))
@paginate
def provinces(request):
    return Province.objects.prefetch_related('nation', 'dioceses', 'injunctions').order_by('label').all()


@api.get("/dioceses/{pk}", response=DioceseSchema)
@decorate_view(cache_page(settings.CACHE_SECONDS))
def diocese(request, pk: int):
    return Diocese.objects.prefetch_related('province', 'province__nation').get(pk=pk)
@api.get("/dioceses", response=PaginatedResponseSchema[DioceseSchema])
@decorate_view(cache_page(settings.CACHE_SECONDS))
@paginate
def dioceses(request):
    return Diocese.objects.prefetch_related('province', 'province__nation').order_by('label').all()


@api.get("/archdeaconries/{pk}", response=ArchdeaconrySchema)
@decorate_view(cache_page(settings.CACHE_SECONDS))
def archdeaconry(request, pk: int):
    return Archdeaconry.objects.prefetch_related('parishes', 'injunctions', 'diocese', 'diocese__province', 'diocese__province__nation').get(pk=pk)
@api.get("/archdeaconries", response=PaginatedResponseSchema[ArchdeaconrySchema])
@decorate_view(cache_page(settings.CACHE_SECONDS))
@paginate
def archdeaconries(request):
    return Archdeaconry.objects.prefetch_related('parishes', 'injunctions', 'diocese', 'diocese__province', 'diocese__province__nation').order_by('label').all()


@api.get("/counties/{pk}", response=CountySchema)
@decorate_view(cache_page(settings.CACHE_SECONDS))
def county(request, pk: int):
    return County.objects.prefetch_related('nation').get(pk=pk)
@api.get("/counties", response=PaginatedResponseSchema[CountySchema])
@decorate_view(cache_page(settings.CACHE_SECONDS))
@paginate
def counties(request):
    return County.objects.prefetch_related('nation').order_by('label').all()



@api.get("/towns/{pk}", response=TownSchema)
@decorate_view(cache_page(settings.CACHE_SECONDS))
def town(request, pk: int):
    return Town.objects.prefetch_related('parishes', 'county', 'county__nation').get(pk=pk)
@api.get("/towns", response=PaginatedResponseSchema[TownSchema])
@decorate_view(cache_page(settings.CACHE_SECONDS))
@paginate
def towns(request):
    return Town.objects.prefetch_related('parishes', 'county', 'county__nation').order_by('label').all()



@api.get("/parishes/{pk}", response=ParishSchema)
@decorate_view(cache_page(settings.CACHE_SECONDS))
def parish(request, pk: int):
    return Parish.objects.prefetch_related(
        'archdeaconry', 'archdeaconry__diocese', 'archdeaconry__diocese__province', 'archdeaconry__diocese__province__nation',
        'town', 'town__county', 'town__county__nation',
    ).get(pk=pk)
@api.get("/parishes", response=PaginatedResponseSchema[ParishSchema])
@decorate_view(cache_page(settings.CACHE_SECONDS))
@paginate(page_size=500)
def parishes(request):
    return Parish.objects.prefetch_related(
        'archdeaconry', 'archdeaconry__diocese', 'archdeaconry__diocese__province', 'archdeaconry__diocese__province__nation',
        'town', 'town__county', 'town__county__nation',
    ).order_by('label').all()



@api.get("/transactions/{pk}", response=TransactionSchema)
@decorate_view(cache_page(settings.CACHE_SECONDS))
def transaction(request, pk: int):
    return Transaction.objects.prefetch_related('transaction_categories').get(pk=pk)
@api.get("/parishes/{parish_id}/transactions", response=PaginatedResponseSchema[TransactionSchema])
@decorate_view(cache_page(settings.CACHE_SECONDS))
@paginate
def parishes_transactions(request, parish_id: int):
    return Transaction.objects.prefetch_related('transaction_categories').filter(parish_id=parish_id).order_by('start_date').all()



@api.get("/inventories/{pk}", response=InventorySchema)
@decorate_view(cache_page(settings.CACHE_SECONDS))
def inventory(request, pk: int):
    return Inventory.objects.get(pk=pk)
@api.get("/parishes/{parish_id}/inventories", response=PaginatedResponseSchema[InventorySchema])
@decorate_view(cache_page(settings.CACHE_SECONDS))
@paginate
def parishes_inventories(request, parish_id: int):
    return Inventory.objects.filter(parish_id=parish_id).order_by('start_date').all()



@api.get("/holdings/{pk}", response=HoldingSchema)
@decorate_view(cache_page(settings.CACHE_SECONDS))
def holding(request, pk: int):
    return Holding.objects.get(pk=pk)
@api.get("/parishes/{parish_id}/holdings", response=PaginatedResponseSchema[HoldingSchema])
@decorate_view(cache_page(settings.CACHE_SECONDS))
@paginate
def parishes_holdings(request, parish_id: int):
    return Holding.objects.filter(parish_id=parish_id).order_by('start_date').all()



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