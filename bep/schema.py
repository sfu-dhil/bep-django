from ninja import Schema, ModelSchema, Field
from typing import List, Optional

from .models import Parish, Transaction, Inventory, Holding, \
    Book, Monarch, \
    Nation, County, Town, Province, Diocese, Archdeaconry

class TransactionSchema(ModelSchema):
    parish_id: Optional[int] = None
    monarch_id: Optional[int] = None
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
    parish_id: Optional[int] = None
    monarch_id: Optional[int] = None
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
    parish_id: Optional[int] = None
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
    monarch_id: Optional[int] = None

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
    nation_id: Optional[int] = None

    class Meta:
        model = County
        fields = ['id', 'label']

class TownSchema(ModelSchema):
    nation_id: Optional[int] = None
    county_id: Optional[int] = None

    class Meta:
        model = Town
        fields = ['id', 'label']

class ProvinceSchema(ModelSchema):
    nation_id: Optional[int] = None

    class Meta:
        model = Province
        fields = ['id', 'label']

class DioceseSchema(ModelSchema):
    nation_id: Optional[int] = None
    province_id: Optional[int] = None

    class Meta:
        model = Diocese
        fields = ['id', 'label']

class ArchdeaconrySchema(ModelSchema):
    nation_id: Optional[int] = None
    province_id: Optional[int] = None
    diocese_id: Optional[int] = None

    class Meta:
        model = Archdeaconry
        fields = ['id', 'label']

class ParishSchema(ModelSchema):
    nation_id: Optional[int] = None
    province_id: Optional[int] = None
    diocese_id: Optional[int] = None
    archdeaconry_id: Optional[int] = None
    county_id: Optional[int] = None
    town_id: Optional[int] = None
    coordinates: Optional[List[float]] = None

    class Meta:
        model = Parish
        fields = [
            'id', 'label', 'description', 'address', 'links',
        ]

    @staticmethod
    def resolve_coordinates(obj):
        return obj.geom_point.coords if obj.geom_point else None

class PointGeometrySchema(Schema):
    type: str = 'Point'
    coordinates: List[float]

class ParishFeaturePropertiesSchema(Schema):
    label: Optional[str] = None
    nation_id: Optional[int] = None
    province_id: Optional[int] = None
    diocese_id: Optional[int] = None
    archdeaconry_id: Optional[int] = None

class ParishFeatureGeoJsonSchema(Schema):
    id: int
    type: str = 'Feature'
    geometry: PointGeometrySchema
    properties: ParishFeaturePropertiesSchema

class ParishFeatureCollectionGeoJsonSchema(Schema):
    type: str = 'FeatureCollection'
    features: List[ParishFeatureGeoJsonSchema]