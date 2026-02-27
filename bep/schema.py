from ninja import Schema, ModelSchema, Field
from typing import List, Optional

from .models import Parish, Transaction, Inventory, Holding, Injunction, \
    Book, Monarch, \
    Nation, County, Town, Province, Diocese, Archdeaconry, \
    TransactionCategory, PrintSource, ManuscriptSource, SourceCategory, Archive

# stubs
class ProvinceStubSchema(ModelSchema):
    class Meta:
        model = Province
        fields = ['id', 'label']
class MonarchStubSchema(ModelSchema):
    class Meta:
        model = Monarch
        fields = ['id', 'label']
class NationStubSchema(ModelSchema):
    class Meta:
        model = Nation
        fields = ['id', 'label']
class CountyStubSchema(ModelSchema):
    class Meta:
        model = County
        fields = ['id', 'label']
class TownStubSchema(ModelSchema):
    class Meta:
        model = Town
        fields = ['id', 'label']
class DioceseStubSchema(ModelSchema):
    class Meta:
        model = Diocese
        fields = ['id', 'label']
class ArchdeaconryStubSchema(ModelSchema):
    class Meta:
        model = Archdeaconry
        fields = ['id', 'label']
class BookStubSchema(ModelSchema):
    monarch: Optional[MonarchStubSchema] = None
    class Meta:
        model = Book
        fields = ['id', 'title']
    @staticmethod
    def resolve_title(obj):
        return f'{obj}'
class ArchiveStubSchema(ModelSchema):
    class Meta:
        model = Archive
        fields = ['id', 'label']
class ParishTransactionStubSchema(ModelSchema):
    class Meta:
        model = Transaction
        fields = ['id', 'start_date', 'end_date']
class SourceCategoryStubSchema(ModelSchema):
    class Meta:
        model = SourceCategory
        fields = ['id', 'label']
class InjunctionStubSchema(ModelSchema):
    class Meta:
        model = Injunction
        fields = ['id', 'title']
class PrintSourceStubSchema(ModelSchema):
    class Meta:
        model = PrintSource
        fields = ['id',  'title']
class ManuscriptSourceStubSchema(ModelSchema):
    class Meta:
        model = ManuscriptSource
        fields = ['id', 'label']

class ParishStubSchema(ModelSchema):
    class Meta:
        model = Parish
        fields = ['id', 'label']

# full records
class MonarchSchema(ModelSchema):
    books: Optional[List[BookStubSchema]]
    class Meta:
        model = Monarch
        fields = ['id', 'label', 'description', 'start_date', 'end_date']

class NationSchema(ModelSchema):
    provinces: Optional[List[ProvinceStubSchema]]
    counties: Optional[List[CountyStubSchema]]
    injunctions: Optional[List[InjunctionStubSchema]]
    class Meta:
        model = Nation
        fields = ['id', 'label', 'description']

class CountySchema(ModelSchema):
    nation: Optional[NationStubSchema] = None
    class Meta:
        model = County
        fields = ['id', 'label', 'description', 'links']

class TownSchema(ModelSchema):
    nation: Optional[NationStubSchema] = None
    county: Optional[CountyStubSchema] = None
    parishes: Optional[List[ParishStubSchema]]
    class Meta:
        model = Town
        fields = ['id', 'label', 'description', 'in_london', 'links']
    @staticmethod
    def resolve_nation(obj):
        return obj.county.nation

class ProvinceSchema(ModelSchema):
    nation: Optional[NationStubSchema] = None
    dioceses: Optional[List[DioceseStubSchema]]
    injunctions: Optional[List[InjunctionStubSchema]]
    class Meta:
        model = Province
        fields = ['id', 'label', 'description', 'links']

class DioceseSchema(ModelSchema):
    nation: Optional[NationStubSchema] = None
    province: Optional[ProvinceStubSchema] = None
    class Meta:
        model = Diocese
        fields = ['id', 'label', 'description']
    @staticmethod
    def resolve_nation(obj):
        return obj.province.nation

class ArchdeaconrySchema(ModelSchema):
    nation: Optional[NationStubSchema] = None
    province: Optional[ProvinceStubSchema] = None
    diocese: Optional[DioceseStubSchema] = None
    parishes: Optional[List[ParishStubSchema]]
    injunctions :Optional[List[InjunctionStubSchema]]
    class Meta:
        model = Archdeaconry
        fields = ['id', 'label', 'description', 'links']
    @staticmethod
    def resolve_nation(obj):
        return obj.diocese.province.nation
    @staticmethod
    def resolve_province(obj):
        return obj.diocese.province

class ParishSchema(ModelSchema):
    nation: Optional[NationStubSchema] = None
    province: Optional[ProvinceStubSchema] = None
    diocese: Optional[DioceseStubSchema] = None
    archdeaconry: Optional[ArchdeaconryStubSchema] = None
    county: Optional[CountyStubSchema] = None
    town: Optional[TownStubSchema] = None
    coordinates: Optional[List[float]] = None
    class Meta:
        model = Parish
        fields = ['id', 'label', 'description', 'address', 'links']
    @staticmethod
    def resolve_nation(obj):
        if obj.archdeaconry and obj.archdeaconry.diocese and obj.archdeaconry.diocese.province and obj.archdeaconry.diocese.province.nation:
            return obj.archdeaconry.diocese.province.nation
        elif obj.town and obj.town.county and obj.town.county.nation:
            return obj.town.county.nation
        return None
    @staticmethod
    def resolve_province(obj):
        return obj.archdeaconry.diocese.province if obj.archdeaconry and obj.archdeaconry.diocese and obj.archdeaconry.diocese.province else None
    @staticmethod
    def resolve_diocese(obj):
        return obj.archdeaconry.diocese if obj.archdeaconry and obj.archdeaconry.diocese else None
    @staticmethod
    def resolve_county(obj):
        return obj.town.county if obj.town and obj.town.county else None
    @staticmethod
    def resolve_coordinates(obj):
        return obj.geom_point.coords if obj.geom_point else None

class BookSchema(ModelSchema):
    monarch: Optional[MonarchStubSchema] = None
    class Meta:
        model = Book
        fields = [
            'id', 'title', 'uniform_title', 'variant_titles', 'author',
            'imprint', 'variant_imprint', 'date', 'estc', 'physical_description', 'description',
            'notes', 'links'
        ]

class ArchiveSchema(ModelSchema):
    class Meta:
        model = Archive
        fields = ['id',  'label', 'description', 'links']

class SourceCategorySchema(ModelSchema):
    manuscript_sources: Optional[List[ManuscriptSourceStubSchema]] = None
    print_sources: Optional[List[PrintSourceStubSchema]] = None
    class Meta:
        model = SourceCategory
        fields = ['id',  'label', 'description']

class PrintSourceSchema(ModelSchema):
    source_category: Optional[SourceCategoryStubSchema] = None
    class Meta:
        model = PrintSource
        fields = ['id',  'title', 'author', 'date', 'publisher', 'notes', 'links']

class ManuscriptSourceSchema(ModelSchema):
    archive: Optional[ArchiveStubSchema] = None
    source_category: Optional[SourceCategoryStubSchema] = None
    class Meta:
        model = ManuscriptSource
        fields = ['id', 'label', 'call_number', 'description', 'links']

class TransactionCategorySchema(ModelSchema):
    class Meta:
        model = TransactionCategory
        fields = ['id',  'label', 'description']

class TransactionSchema(ModelSchema):
    class Meta:
        model = Transaction
        fields = [
            'id', 'start_date', 'end_date', 'written_date',
            # 'value', 'shipping', 'copies', 'location', 'page', 'transcription', 'modern_transcription', 'public_notes',
            # 'injunction_id', 'monarch_id', 'manuscript_source_id', 'print_source_id'
        ]

class ParishInventoryStubSchema(ModelSchema):
    class Meta:
        model = Inventory
        fields = ['id', 'start_date', 'end_date']
class InventorySchema(ModelSchema):
    class Meta:
        model = Inventory
        fields = [
            'id',  'start_date', 'end_date', 'written_date',
            # 'page_number', 'transcription', 'modifications', 'description',
            # 'injunction_id', 'monarch_id', 'manuscript_source_id', 'print_source_id'
        ]

class ParishHoldingStubSchema(ModelSchema):
    class Meta:
        model = Holding
        fields = ['id', 'start_date', 'end_date']
class HoldingSchema(ModelSchema):
    class Meta:
        model = Holding
        fields = [
            'id', 'start_date', 'end_date', 'written_date', 'description',
        ]


class InjunctionSchema(ModelSchema):
    nation: Optional[NationStubSchema] = None
    province: Optional[ProvinceStubSchema] = None
    diocese: Optional[DioceseStubSchema] = None
    archdeaconry: Optional[ArchdeaconryStubSchema] = None
    monarch: Optional[MonarchStubSchema] = None
    class Meta:
        model = Injunction
        fields = [
            'id', 'title', 'uniform_title', 'variant_titles', 'author',
            'imprint', 'variant_imprint', 'estc', 'date', 'physical_description',
            'transcription', 'modern_transcription', 'notes', 'links',
        ]


# GeoJson
class PointGeometrySchema(Schema):
    type: str = 'Point'
    coordinates: List[float]

class ParishFeaturePropertiesSchema(Schema):
    label: Optional[str] = None
    county_id: Optional[int] = None
    # nation_id: Optional[int] = None
    # province_id: Optional[int] = None
    # diocese_id: Optional[int] = None
    # archdeaconry_id: Optional[int] = None

class ParishFeatureGeoJsonSchema(Schema):
    id: int
    type: str = 'Feature'
    geometry: PointGeometrySchema
    properties: ParishFeaturePropertiesSchema

class ParishFeatureCollectionGeoJsonSchema(Schema):
    type: str = 'FeatureCollection'
    features: List[ParishFeatureGeoJsonSchema]