from ninja_extra import NinjaExtraAPI
from ninja_extra.pagination import paginate, PaginatedResponseSchema
from ninja.decorators import decorate_view
from django.views.decorators.cache import cache_page
from django.conf import settings
from django.db.models import Q

from .schema import *
from .models import Parish, Transaction, Inventory, Holding, \
    Book, Monarch, \
    Nation, County, Town, Province, Diocese, Archdeaconry

api = NinjaExtraAPI(title='Books in English Parishes API')

@api.get("/transactions", response=PaginatedResponseSchema[TransactionSchema], url_name='transactions')
@paginate
@decorate_view(cache_page(settings.CACHE_SECONDS))
def transactions(request):
    return Transaction.objects.prefetch_related('parish', 'monarch', 'books').order_by('start_date').all()

@api.get("/inventories", response=PaginatedResponseSchema[InventorySchema], url_name='inventories')
@paginate
@decorate_view(cache_page(settings.CACHE_SECONDS))
def inventories(request):
    return Inventory.objects.prefetch_related('parish', 'monarch', 'books').order_by('start_date').all()

@api.get("/holdings", response=PaginatedResponseSchema[HoldingSchema], url_name='holdings')
@paginate
@decorate_view(cache_page(settings.CACHE_SECONDS))
def holdings(request):
    return Holding.objects.prefetch_related('parish', 'books').order_by('start_date').all()

@api.get("/books", response=PaginatedResponseSchema[BookSchema], url_name='books')
@paginate
@decorate_view(cache_page(settings.CACHE_SECONDS))
def books(request):
    return Book.objects.prefetch_related('monarch').order_by('title', 'date').all()

@api.get("/monarchs", response=PaginatedResponseSchema[MonarchSchema], url_name='monarchs')
@paginate
@decorate_view(cache_page(settings.CACHE_SECONDS))
def monarchs(request):
    return Monarch.objects.order_by('start_date').all()

@api.get("/nations", response=PaginatedResponseSchema[NationSchema], url_name='nations')
@paginate
@decorate_view(cache_page(settings.CACHE_SECONDS))
def nations(request):
    return Nation.objects \
        .filter(Q(counties__towns__parishes__latitude__isnull=False) | Q(provinces__dioceses__archdeaconries__parishes__latitude__isnull=False)) \
        .distinct() \
        .order_by('label').all()

@api.get("/counties", response=PaginatedResponseSchema[CountySchema], url_name='counties')
@paginate
@decorate_view(cache_page(settings.CACHE_SECONDS))
def counties(request):
    return County.objects.prefetch_related('nation') \
        .filter(towns__parishes__latitude__isnull=False) \
        .distinct() \
        .order_by('label').all()

@api.get("/towns", response=PaginatedResponseSchema[TownSchema], url_name='towns')
@paginate
@decorate_view(cache_page(settings.CACHE_SECONDS))
def towns(request):
    return Town.objects.select_related('county', 'county__nation') \
        .filter(parishes__latitude__isnull=False) \
        .distinct() \
        .order_by('label').all()

@api.get("/provinces", response=PaginatedResponseSchema[ProvinceSchema], url_name='provinces')
@paginate
@decorate_view(cache_page(settings.CACHE_SECONDS))
def provinces(request):
    return Province.objects.prefetch_related('nation') \
        .filter(dioceses__archdeaconries__parishes__latitude__isnull=False) \
        .distinct() \
        .order_by('label').all()

@api.get("/dioceses", response=PaginatedResponseSchema[DioceseSchema], url_name='dioceses')
@paginate
@decorate_view(cache_page(settings.CACHE_SECONDS))
def dioceses(request):
    return Diocese.objects.select_related('province', 'province__nation') \
        .filter(archdeaconries__parishes__latitude__isnull=False) \
        .distinct() \
        .order_by('label').all()

@api.get("/archdeaconries", response=PaginatedResponseSchema[ArchdeaconrySchema], url_name='archdeaconries')
@paginate
@decorate_view(cache_page(settings.CACHE_SECONDS))
def archdeaconries(request):
    return Archdeaconry.objects.select_related('diocese', 'diocese__province', 'diocese__province__nation') \
        .filter(parishes__latitude__isnull=False) \
        .distinct() \
        .order_by('label').all()

@api.get("/parishes", response=PaginatedResponseSchema[ParishSchema], url_name='parishes')
@paginate
@decorate_view(cache_page(settings.CACHE_SECONDS))
def parishes(request):
    return Parish.objects.select_related(
        'archdeaconry', 'archdeaconry__diocese', 'archdeaconry__diocese__province', 'archdeaconry__diocese__province__nation',
        'town', 'town__county',  'town__county__nation',
    ) \
        .filter(latitude__isnull=False) \
        .filter(longitude__isnull=False) \
        .order_by('label').all()
