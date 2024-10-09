from rest_framework import serializers
from .models import Book, Monarch, Transaction, Inventory, Holding


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = [
            'id', 'start_date', 'written_date', 'parish_id', 'monarch_id', 'books',
            # 'value', 'shipping', 'copies', 'location', 'page', 'transcription', 'modern_transcription', 'public_notes',
            # 'injunction_id', 'monarch_id', 'manuscript_source_id', 'print_source_id'
        ]
        read_only = True

class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = [
            'id',  'start_date', 'written_date', 'parish_id', 'monarch_id', 'books',
            # 'page_number', 'transcription', 'modifications', 'description',
            # 'injunction_id', 'monarch_id', 'manuscript_source_id', 'print_source_id'
        ]

class HoldingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Holding
        fields = [
            'id', 'start_date', 'written_date',  'parish_id', 'books',
            'description',
            # 'archive_id'
        ]
        read_only = True

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'date', 'monarch_id']
        read_only = True

class MonarchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Monarch
        fields = ['id', 'label', 'start_date', 'end_date']
        read_only = True

class NationSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    label = serializers.CharField()

    class Meta:
        read_only = True

class CountySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    label = serializers.CharField()
    nation_id = serializers.IntegerField()

    class Meta:
        read_only = True


class TownSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    label = serializers.CharField()
    county_id = serializers.IntegerField()
    nation_id = serializers.IntegerField(source='county__nation_id')

    class Meta:
        read_only = True

class ProvinceSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    label = serializers.CharField()
    nation_id = serializers.IntegerField()

    class Meta:
        read_only = True

class DioceseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    label = serializers.CharField()
    province_id = serializers.IntegerField()
    nation_id = serializers.IntegerField(source='province__nation_id')

    class Meta:
        read_only = True

class ArchdeaconrySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    label = serializers.CharField()
    diocese_id = serializers.IntegerField()
    province_id = serializers.IntegerField(source='diocese__province_id')
    nation_id = serializers.IntegerField(source='diocese__province__nation_id')

    class Meta:
        read_only = True

class ParishSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    label = serializers.CharField()
    description = serializers.CharField()
    address = serializers.CharField()
    links = serializers.ListField(child=serializers.CharField(), allow_empty=True)
    latitude = serializers.DecimalField(max_digits=10, decimal_places=7)
    longitude = serializers.DecimalField(max_digits=10, decimal_places=7)
    archdeaconry_id = serializers.IntegerField()
    diocese_id = serializers.IntegerField(source='archdeaconry__diocese_id')
    province_id = serializers.IntegerField(source='archdeaconry__diocese__province_id')
    town_id = serializers.IntegerField()
    county_id = serializers.IntegerField(source='town__county_id')
    nation_id = serializers.SerializerMethodField()

    class Meta:
        read_only = True

    def get_nation_id(self, dict):
        return dict.get('town__county__nation_id', dict.get('archdeaconry__diocese__province__nation_id'))