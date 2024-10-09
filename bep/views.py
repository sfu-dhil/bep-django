from django.shortcuts import render
from django.views.decorators.cache import cache_page
from rest_framework.renderers import JSONRenderer
from django.conf import settings
from .models import Parish, Transaction, Inventory, Holding, \
    Book, Monarch, \
    Nation, County, Town, Province, Diocese, Archdeaconry
from .serializers import TransactionSerializer, InventorySerializer, HoldingSerializer, \
    BookSerializer, MonarchSerializer, \
    ParishSerializer, ArchdeaconrySerializer, DioceseSerializer, ProvinceSerializer, \
    TownSerializer, CountySerializer, NationSerializer \

@cache_page(settings.CACHE_SECONDS)
def dashboard(request):

    return render(request, 'dashboard.html', {
        'transactions': TransactionSerializer(
            Transaction.objects.prefetch_related('books').order_by('start_date').all(),
            many=True
        ).data,
        'inventories': InventorySerializer(
            Inventory.objects.prefetch_related('books').order_by('start_date').all(),
            many=True
        ).data,
        'holdings': HoldingSerializer(
            Holding.objects.prefetch_related('books').order_by('start_date').all(),
            many=True
        ).data,
        'books': BookSerializer(
            Book.objects.order_by('title', 'date').all(),
            many=True
        ).data,
        'monarchs': MonarchSerializer(
            Monarch.objects.order_by('start_date').all(),
            many=True
        ).data,
        'nations': NationSerializer(
            Nation.objects.values('id', 'label').order_by('label').all(),
            many=True
        ).data,
        'counties': CountySerializer(
            County.objects.values('id', 'label', 'nation_id').order_by('label').all(),
            many=True
        ).data,
        'towns': TownSerializer(
            Town.objects.select_related('county').values('id', 'label', 'county_id', 'county__nation_id').order_by('label').all(),
            many=True
        ).data,
        'provinces': ProvinceSerializer(
            Province.objects.values('id', 'label', 'nation_id').order_by('label').all(),
            many=True
        ).data,
        'dioceses': DioceseSerializer(
            Diocese.objects.select_related('province').values('id', 'label', 'province_id', 'province__nation_id').order_by('label').all(),
            many=True
        ).data,
        'archdeaconries': ArchdeaconrySerializer(
            Archdeaconry.objects.select_related('diocese', 'diocese__province').values('id', 'label', 'diocese_id', 'diocese__province_id', 'diocese__province__nation_id').order_by('label').all(),
            many=True
        ).data,
        'parishes': ParishSerializer(
            Parish.objects.select_related(
                'archdeaconries', 'archdeaconries__diocese', 'diocese__province',
                'town', 'town__county'
            ).values(
                'id', 'label', 'latitude', 'longitude',
                'description', 'address', 'links',
                'archdeaconry_id', 'archdeaconry__diocese_id', 'archdeaconry__diocese__province_id', 'archdeaconry__diocese__province__nation_id',
                'town_id', 'town__county_id', 'town__county__nation_id'
            ).order_by('label').all(),
            many=True
        ).data,
    })