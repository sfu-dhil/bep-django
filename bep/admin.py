from django.contrib import admin
from django.db import models
from django.utils.safestring import mark_safe
from django.contrib.admin import ModelAdmin, TabularInline, StackedInline
from tinymce.widgets import TinyMCE
from modelclone import ClonableModelAdmin
from bep.widgets import Select2TagArrayWidget
from leaflet.admin import LeafletGeoAdmin

from .models import Archdeaconry, Archive, Book, Holding, ManuscriptSource, Parish, \
    Injunction, Transaction, Inventory, County, Town, Diocese, InventoryImage, HoldingImage, \
    Monarch, Nation, Province, PrintSource, Format, SourceCategory, TransactionCategory
from .forms import TransactionAdminForm


# Inlines (used by admin panel items)
class ReadOnlyTabularInline(TabularInline):
    show_change_link = True
    def has_change_permission(self, request, obj=None):
        return False
    def has_add_permission(self, request, obj):
        return False
    def has_delete_permission(self, request, obj):
        return False
    classes = ['collapse']

class SimpleTermReadOnlyInline(ReadOnlyTabularInline):
    ordering = ['label']
    exclude = ['description', 'links']
    readonly_fields = ['_description']

    def _description(self, obj):
        return mark_safe(obj.description)
    _description.short_description = 'Description'

class ManuscriptSourceReadOnlyInline(SimpleTermReadOnlyInline):
    model = ManuscriptSource

class ParishReadOnlyInline(SimpleTermReadOnlyInline):
    model = Parish

class TownReadOnlyInline(SimpleTermReadOnlyInline):
    model = Town

class ArchdeaconryReadOnlyInline(SimpleTermReadOnlyInline):
    model = Archdeaconry

class CountyReadOnlyInline(SimpleTermReadOnlyInline):
    model = County

class ProvinceReadOnlyInline(SimpleTermReadOnlyInline):
    model = Province

class DioceseReadOnlyInline(SimpleTermReadOnlyInline):
    model = Diocese

class HoldingReadOnlyInline(ReadOnlyTabularInline):
    exclude = ['notes', 'books']
    ordering = ['description']
    exclude = ['description']
    readonly_fields = ['_description']
    model = Holding

    def _description(self, obj):
        return mark_safe(obj.description)
    _description.short_description = 'Description'

class InjunctionReadOnlyInline(ReadOnlyTabularInline):
    exclude = ['imprint', 'transcription', 'modern_transcription', 'notes', 'physical_description']
    ordering = ['title']
    readonly_fields = ['_physical_description']
    model = Injunction

    def _physical_description(self, obj):
        return mark_safe(obj.physical_description)
    _physical_description.short_description = 'Physical Description'


class TransactionReadOnlyInline(ReadOnlyTabularInline):
    fields = ['written_date', '_value', 'copies', 'location']
    ordering = ['id']
    readonly_fields = ['_value']
    model = Transaction

    def _value(self, obj):
        return Transaction.get_lsd_str(obj.value)
    _value.short_description = 'Value'

class InventoryReadOnlyInline(ReadOnlyTabularInline):
    exclude = ['notes', 'transcription', 'description', 'modifications']
    ordering = ['transcription']
    readonly_fields = ['_transcription', '_description', '_modifications']
    model = Inventory

    def _transcription(self, obj):
        return mark_safe(obj.transcription)
    _transcription.short_description = 'Transcription'

    def _description(self, obj):
        return mark_safe(obj.description)
    _description.short_description = 'Description'

    def _modifications(self, obj):
        return mark_safe(obj.modifications)
    _modifications.short_description = 'Modifications'

class BookReadOnlyInline(ReadOnlyTabularInline):
    fields = ['_title', '_uniform_title', 'author', '_imprint', 'date']
    ordering = ['title']
    readonly_fields = ['_title', '_uniform_title', '_imprint']
    model = Book

    def _title(self, obj):
        return mark_safe(obj.title)
    _title.short_description = 'Title'

    def _uniform_title(self, obj):
        return mark_safe(obj.uniform_title)
    _uniform_title.short_description = 'Uniform Title'

    def _imprint(self, obj):
        return mark_safe(obj.imprint)
    _imprint.short_description = 'Imprint'

class PrintSourceReadOnlyInline(ReadOnlyTabularInline):
    fields = ['title', 'author', 'date', 'publisher']
    ordering = ['title']
    model = PrintSource

# Inlines for Many-toMany
class BookM2MTransactionReadOnlyInline(ReadOnlyTabularInline):
    model = Book.transactions.through
    verbose_name = 'Transaction'

class BookM2MInventoryReadOnlyInline(ReadOnlyTabularInline):
    model = Book.inventories.through
    verbose_name = 'Inventory'
    verbose_name_plural = 'inventories'

class BookM2MHoldingReadOnlyInline(ReadOnlyTabularInline):
    model = Book.holdings.through
    verbose_name = 'surviving text'

class TransactionCategoryM2MTransactionReadOnlyInline(ReadOnlyTabularInline):
    model = TransactionCategory.transactions.through
    verbose_name = 'transaction'

# Image Inlines
class InventoryImageInline(StackedInline):
    fields = ['image', 'description', 'license']
    ordering = ['id']
    model = InventoryImage
    extra=0
class HoldingImageInline(StackedInline):
    fields = ['image', 'description', 'license']
    ordering = ['id']
    model = HoldingImage
    extra=0

# Admin Panel Items
class BepAdminDefaults(ModelAdmin):
    compressed_fields = True

    # all list displayed fields are display links
    def get_list_display_links(self, request, list_display):
        return self.list_display

    formfield_overrides = {
        models.TextField: {
            "widget": TinyMCE,
        },
    }

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'links':
            kwargs['widget'] = Select2TagArrayWidget(attrs={
                'data-placeholder': 'Click to add one or more links',
            })
        elif db_field.name == 'variant_titles':
            kwargs['widget'] = Select2TagArrayWidget(attrs={
                'data-placeholder': 'Click to add one or more variant title',
            })
        return super().formfield_for_dbfield(db_field, **kwargs)

class SimpleTermModelDefaults(BepAdminDefaults):
    list_display = ['label', '_description']
    search_fields = ['label', 'description']
    ordering = ['label']

    def _description(self, obj):
        return mark_safe(obj.description)
    _description.short_description = 'Description'
    _description.admin_order_field = 'description'

@admin.register(Archdeaconry)
class ArchdeaconryAdmin(SimpleTermModelDefaults):
    autocomplete_fields = ['diocese']
    inlines = [
        ParishReadOnlyInline,
        InjunctionReadOnlyInline,
    ]


@admin.register(Archive)
class ArchiveAdmin(SimpleTermModelDefaults):
    inlines = [
        ManuscriptSourceReadOnlyInline,
        HoldingReadOnlyInline,
    ]

@admin.register(Book)
class BookAdmin(BepAdminDefaults):
    list_display = ['_title', '_uniform_title', 'author', '_imprint', 'date', 'monarch']
    search_fields = ['title', 'uniform_title', 'author', 'imprint', 'date']
    ordering = ['title']

    autocomplete_fields = ['format', 'monarch']
    inlines = [
        BookM2MTransactionReadOnlyInline,
        BookM2MInventoryReadOnlyInline,
        BookM2MHoldingReadOnlyInline,
    ]

    def _title(self, obj):
        return obj.title if len(obj.title) <= 100 else obj.title[:100].rsplit(' ', 1)[0] + '...'
    _title.short_description = 'Title'
    _title.admin_order_field = 'title'

    def _uniform_title(self, obj):
        return obj.uniform_title if len(obj.uniform_title) <= 100 else obj.uniform_title[:100].rsplit(' ', 1)[0] + '...'
    _uniform_title.short_description = 'Uniform Title'
    _uniform_title.admin_order_field = 'uniform_title'

    def _imprint(self, obj):
        return mark_safe(obj.imprint)
    _imprint.short_description = 'Imprint'
    _imprint.admin_order_field = 'imprint'

@admin.register(County)
class CountyAdmin(SimpleTermModelDefaults):
    autocomplete_fields = ['nation']
    inlines = [
        TownReadOnlyInline,
    ]

@admin.register(Diocese)
class DioceseAdmin(SimpleTermModelDefaults, LeafletGeoAdmin):
    autocomplete_fields = ['province']
    inlines = [
        ArchdeaconryReadOnlyInline,
        InjunctionReadOnlyInline,
    ]

@admin.register(Injunction)
class InjunctionAdmin(BepAdminDefaults):
    list_display = ['_title', 'date', 'monarch', '_transcription']
    search_fields = ['title', 'date', 'transcription']
    ordering = ['title']

    autocomplete_fields = ['nation', 'diocese', 'province', 'archdeaconry', 'monarch']
    inlines = [
        TransactionReadOnlyInline,
        InventoryReadOnlyInline,
    ]

    def _title(self, obj):
        return mark_safe(obj.title)
    _title.short_description = 'Title'
    _title.admin_order_field = 'title'

    def _transcription(self, obj):
        return mark_safe(obj.transcription)
    _transcription.short_description = 'Transcription'
    _transcription.admin_order_field = 'transcription'


@admin.register(Inventory)
class InventoryAdmin(BepAdminDefaults):
    list_display = ['_id', '_date', '_transcription', 'parish', 'print_source', '_books']
    search_fields = ['id', 'transcription']
    ordering = ['id']

    autocomplete_fields = ['manuscript_source', 'print_source', 'parish', 'monarch', 'injunction', 'books']
    inlines = [
        InventoryImageInline,
    ]

    def _id(self, obj):
        return f"{obj.id:05d}"
    _id.short_description = 'ID'
    _id.admin_order_field = 'id'

    def _transcription(self, obj):
        return f"{obj}"
    _transcription.short_description = 'Transcription'
    _transcription.admin_order_field = 'transcription'

    def _date(self, obj):
        if obj.start_date and obj.end_date:
            return f"{obj.start_date}-{obj.end_date}"
        elif obj.start_date:
            return f"{obj.start_date}"
        elif obj.end_date:
            return f"{obj.end_date}"
        return None
    _date.short_description = 'Date'
    _date.admin_order_field = 'start_date'

    def _books(self, obj):
        return obj.books.count()
    _books.short_description = 'Books'
    _books.admin_order_field = 'books__count'


@admin.register(ManuscriptSource)
class ManuscriptSourceAdmin(SimpleTermModelDefaults):
    autocomplete_fields = ['source_category', 'archive']
    inlines = [
        TransactionReadOnlyInline,
        InventoryReadOnlyInline,
    ]

@admin.register(Monarch)
class MonarchAdmin(SimpleTermModelDefaults):
    inlines = [
        TransactionReadOnlyInline,
        InjunctionReadOnlyInline,
        InventoryReadOnlyInline,
        BookReadOnlyInline,
    ]

@admin.register(Nation)
class NationAdmin(SimpleTermModelDefaults):
    inlines = [
        ProvinceReadOnlyInline,
        CountyReadOnlyInline,
        InjunctionReadOnlyInline,
    ]

@admin.register(Parish)
class ParishAdmin(SimpleTermModelDefaults):
    autocomplete_fields = ['archdeaconry', 'town']
    inlines = [
        TransactionReadOnlyInline,
        InventoryReadOnlyInline,
        HoldingReadOnlyInline,
    ]

@admin.register(PrintSource)
class PrintSourceAdmin(BepAdminDefaults):
    list_display = ['title', 'date', 'author', 'publisher']
    search_fields = ['title', 'date', 'transcription']
    ordering = ['title']

    autocomplete_fields = ['source_category']
    inlines = [
        TransactionReadOnlyInline,
        InventoryReadOnlyInline,
    ]

@admin.register(Province)
class ProvinceAdmin(SimpleTermModelDefaults):
    autocomplete_fields = ['nation']
    inlines = [
        DioceseReadOnlyInline,
        InjunctionReadOnlyInline,
    ]

@admin.register(Town)
class TownAdmin(SimpleTermModelDefaults):
    autocomplete_fields = ['county']
    inlines = [
        ParishReadOnlyInline,
    ]

@admin.register(Transaction)
class TransactionAdmin(ClonableModelAdmin, BepAdminDefaults):
    clone_verbose_name = 'Create new copy of transaction'
    form = TransactionAdminForm
    list_display = ['_id', '_date', 'manuscript_source', '_value', '_books', 'parish', '_modern_transcription']
    search_fields = ['id', 'written_date', 'value', 'modern_transcription']
    ordering = ['id']

    autocomplete_fields = ['parish', 'manuscript_source', 'print_source', 'injunction', 'monarch', 'transaction_categories', 'books']

    fields = [
        ('value_l', 'value_s', 'value_d'),
        ('shipping_l', 'shipping_s', 'shipping_d'),
        'copies',
        'location',
        'page',
        'transcription',
        'modern_transcription',
        'public_notes',
        'notes',
        'start_date',
        'end_date',
        'written_date',
        'parish',
        'manuscript_source',
        'print_source',
        'injunction',
        'monarch',
        'transaction_categories',
        'books',
    ]

    def _id(self, obj):
        return f"{obj.id:05d}"
    _id.short_description = 'ID'
    _id.admin_order_field = 'id'

    def _date(self, obj):
        if obj.written_date:
            return mark_safe(obj.written_date)
        if obj.start_date and obj.end_date:
            return f"{obj.start_date}-{obj.end_date}"
        elif obj.start_date:
            return f"{obj.start_date}"
        return 'No date'
    _date.short_description = 'Date'

    def _value(self, obj):
        return Transaction.get_lsd_str(obj.value)
    _value.short_description = 'Value'
    _value.admin_order_field = models.F('value').desc(nulls_last=True)

    def _books(self, obj):
        return obj.books.count()
    _books.short_description = 'Books'
    _books.admin_order_field = 'books__count'

    def _modern_transcription(self, obj):
        return mark_safe(obj.modern_transcription)
    _modern_transcription.short_description = 'Modern English'
    _modern_transcription.admin_order_field = 'modern_transcription'

@admin.register(Holding)
class HoldingAdmin(BepAdminDefaults):
    list_display = ['_date', 'parish', '_book']
    search_fields = ['start_date', 'end_date', 'written_date', 'description']
    ordering = ['start_date']
    autocomplete_fields = ['parish', 'archive', 'books']
    inlines = [
        HoldingImageInline,
    ]

    def _date(self, obj):
        if obj.start_date and obj.end_date:
            return f"{obj.start_date}-{obj.end_date}"
        elif obj.start_date:
            return f"{obj.start_date}"
        elif obj.written_date:
            return obj.written_date
        return 'No date'
    _date.short_description = 'Date & Source'

    def _modern_transcription(self, obj):
        return mark_safe(obj.modern_transcription)
    _modern_transcription.short_description = 'Modern English'
    _modern_transcription.admin_order_field = 'modern_transcription'

    def _book(self, obj):
        return mark_safe('<br>'.join(
            [str(n) for n in obj.books.all()]
        ))
    _book.short_description = 'Book'

@admin.register(Format)
class FormatAdmin(SimpleTermModelDefaults):
    inlines = [
        BookReadOnlyInline,
    ]

@admin.register(SourceCategory)
class SourceCategoryAdmin(SimpleTermModelDefaults):
    inlines = [
        ManuscriptSourceReadOnlyInline,
        PrintSourceReadOnlyInline,
    ]

@admin.register(TransactionCategory)
class TransactionCategoryAdmin(SimpleTermModelDefaults):
    inlines = [
        TransactionCategoryM2MTransactionReadOnlyInline,
    ]