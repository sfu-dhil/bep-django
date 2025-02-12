from ninja import ModelSchema, Field
from typing import List, Optional

from .models import Parish, Transaction, Inventory, Holding, \
    Book, Monarch, \
    Nation, County, Town, Province, Diocese, Archdeaconry

class TransactionSchema(ModelSchema):
    parish_id: int = Field(None, alias="parish.id")
    monarch_id: int = Field(None, alias="monarch.id")
    books: List[int] = []

    class Meta:
        model = Transaction
        fields = [
            'id', 'start_date', 'end_date', 'written_date',
            # 'value', 'shipping', 'copies', 'location', 'page', 'transcription', 'modern_transcription', 'public_notes',
            # 'injunction_id', 'monarch_id', 'manuscript_source_id', 'print_source_id'
        ]

    @staticmethod
    def resolve_books(obj):
         return [book.id for book in obj.books.all()]

class InventorySchema(ModelSchema):
    parish_id: int = Field(None, alias="parish.id")
    monarch_id: int = Field(None, alias="monarch.id")
    books: List[int] = []

    class Meta:
        model = Inventory
        fields = [
            'id',  'start_date', 'end_date', 'written_date',
            # 'page_number', 'transcription', 'modifications', 'description',
            # 'injunction_id', 'monarch_id', 'manuscript_source_id', 'print_source_id'
        ]

    @staticmethod
    def resolve_books(obj):
         return [book.id for book in obj.books.all()]

class HoldingSchema(ModelSchema):
    parish_id: int = Field(None, alias="parish.id")
    books: List[int] = []

    class Meta:
        model = Holding
        fields = [
            'id', 'start_date', 'end_date', 'written_date',
            'description',
            # 'archive_id'
        ]

    @staticmethod
    def resolve_books(obj):
         return [book.id for book in obj.books.all()]

class BookSchema(ModelSchema):
    monarch_id: int = Field(None, alias="monarch.id")

    class Meta:
        model = Book
        fields = ['id', 'title', 'date']

class MonarchSchema(ModelSchema):
    class Meta:
        model = Monarch
        fields = ['id', 'label', 'start_date', 'end_date']

class NationSchema(ModelSchema):
    class Meta:
        model = Nation
        fields = ['id', 'label']

class CountySchema(ModelSchema):
    nation_id: int = Field(None, alias="nation.id")

    class Meta:
        model = County
        fields = ['id', 'label']

class TownSchema(ModelSchema):
    nation_id: int = Field(None, alias='county.nation.id')
    county_id: int = Field(None, alias='county.id')

    class Meta:
        model = Town
        fields = ['id', 'label']

class ProvinceSchema(ModelSchema):
    nation_id: int = Field(None, alias="nation.id")

    class Meta:
        model = Province
        fields = ['id', 'label']

class DioceseSchema(ModelSchema):
    nation_id: int = Field(None, alias='province.nation.id')
    province_id: int = Field(None, alias='province.id')

    class Meta:
        model = Diocese
        fields = ['id', 'label']

class ArchdeaconrySchema(ModelSchema):
    nation_id: int = Field(None, alias='diocese.province.nation.id')
    province_id: int = Field(None, alias='diocese.province.id')
    diocese_id: int = Field(None, alias='diocese.id')

    class Meta:
        model = Archdeaconry
        fields = ['id', 'label']

class ParishSchema(ModelSchema):
    nation_id: int = None
    province_id: int = Field(None, alias='archdeaconry.diocese.province.id')
    diocese_id: int = Field(None, alias='archdeaconry.diocese.id')
    archdeaconry_id: int = Field(None, alias='archdeaconry.id')
    county_id: int = Field(None, alias='town.county.id')
    town_id: int = Field(None, alias='town.id')
    coordinates: Optional[List[float]] = None

    class Meta:
        model = Parish
        fields = [
            'id', 'label', 'description', 'address', 'links',
        ]

    @staticmethod
    def resolve_nation_id(obj):
        if obj.archdeaconry.diocese.province.nation.id:
            return obj.archdeaconry.diocese.province.nation.id
        # fall back on town->county->nation if there is a break in the archdeaconry chain
        if obj.town.county.nation.id:
            return obj.town.county.nation.id

    @staticmethod
    def resolve_coordinates(obj):
        if obj.latitude and obj.longitude:
            try:
                return [float(obj.longitude), float(obj.latitude)]
            except ValueError:
                return None