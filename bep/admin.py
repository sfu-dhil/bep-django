from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin, UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group, User
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.safestring import mark_safe
from html import unescape
from unfold.admin import ModelAdmin, TabularInline, StackedInline
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm
from unfold.contrib.forms.widgets import ArrayWidget, WysiwygWidget
from unfold.decorators import display
from modelclone import ClonableModelAdmin

from .models import Archdeaconry, Archive, Book, Holding, ManuscriptSource, Parish, \
    Injunction, Transaction, Inventory, County, Town, Diocese, InventoryImage, HoldingImage, \
    Monarch, Nation, Province, PrintSource, Format, SourceCategory, TransactionCategory
from .forms import TransactionAdminForm

# override the Auth User and Group models to use unfold UI theme
admin.site.unregister(User)
@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm

admin.site.unregister(Group)
@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass


# Inlines (used by admin panel items)
class ReadOnlyTabularInline(TabularInline):
    show_change_link = True
    def has_change_permission(self, request, obj=None):
        return False
    def has_add_permission(self, request, obj):
        return False
    def has_delete_permission(self, request, obj):
        return False

class SimpleTermReadOnlyInline(ReadOnlyTabularInline):
    ordering = ['label']
    readonly_preprocess_fields = {
        "description": lambda contents: mark_safe(unescape(contents)),
    }

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
    readonly_preprocess_fields = {
        "description": lambda contents: mark_safe(unescape(contents)),
    }
    model = Holding

class InjunctionReadOnlyInline(ReadOnlyTabularInline):
    exclude = ['imprint', 'transcription', 'modern_transcription', 'notes']
    ordering = ['title']
    readonly_preprocess_fields = {
        "physical_description": lambda contents: mark_safe(unescape(contents)),
    }
    model = Injunction

class TransactionReadOnlyInline(ReadOnlyTabularInline):
    fields = ['written_date', 'value', 'copies', 'location']
    ordering = ['id']
    model = Transaction

    readonly_preprocess_fields = {
        "value": lambda contents: Transaction.get_lsd_str(contents),
    }

class InventoryReadOnlyInline(ReadOnlyTabularInline):
    exclude = ['notes']
    ordering = ['transcription']
    readonly_preprocess_fields = {
        "transcription": lambda contents: mark_safe(unescape(contents)),
        "description": lambda contents: mark_safe(unescape(contents)),
        "modifications": lambda contents: mark_safe(unescape(contents)),
    }

    model = Inventory

class BookReadOnlyInline(ReadOnlyTabularInline):
    fields = ['title', 'uniform_title', 'author', 'imprint', 'date']
    ordering = ['title']
    readonly_preprocess_fields = {
        "title": lambda contents: mark_safe(unescape(contents)),
        "uniform_title": lambda contents: mark_safe(unescape(contents)),
        "imprint": lambda contents: mark_safe(unescape(contents)),
    }
    model = Book

class PrintSourceReadOnlyInline(ReadOnlyTabularInline):
    fields = ['title', 'author', 'date', 'publisher']
    ordering = ['title']
    model = PrintSource

# Inlines for Many-toMany
class BookM2MTransactionReadOnlyInline(ReadOnlyTabularInline):
    model = Book.transactions.through

class BookM2MInventoryReadOnlyInline(ReadOnlyTabularInline):
    model = Book.inventories.through

class BookM2MHoldingReadOnlyInline(ReadOnlyTabularInline):
    model = Book.holdings.through

class TransactionCategoryM2MTransactionReadOnlyInline(ReadOnlyTabularInline):
    model = TransactionCategory.transactions.through

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
            "widget": WysiwygWidget,
        },
        ArrayField: {
            "widget": ArrayWidget,
        }
    }


class SimpleTermModelDefaults(BepAdminDefaults):
    list_display = ['label', '_description']
    search_fields = ['label', 'description']
    ordering = ['label']

    @display(description="Description", ordering="description")
    def _description(self, obj):
        return mark_safe(obj.description)

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

    @display(description="Title", ordering="title")
    def _title(self, obj):
        return obj.title if len(obj.title) <= 100 else obj.title[:100].rsplit(' ', 1)[0] + '...'

    @display(description="Uniform Title", ordering="uniform_title")
    def _uniform_title(self, obj):
        return obj.uniform_title if len(obj.uniform_title) <= 100 else obj.uniform_title[:100].rsplit(' ', 1)[0] + '...'

    @display(description="Imprint", ordering="imprint")
    def _imprint(self, obj):
        return mark_safe(obj.imprint)

@admin.register(County)
class CountyAdmin(SimpleTermModelDefaults):
    autocomplete_fields = ['nation']
    inlines = [
        TownReadOnlyInline,
    ]

@admin.register(Diocese)
class DioceseAdmin(SimpleTermModelDefaults):
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

    @display(description="Title", ordering="title")
    def _title(self, obj):
        return mark_safe(obj.title)

    @display(description="Transcription", ordering="transcription")
    def _transcription(self, obj):
        return mark_safe(obj.transcription)


@admin.register(Inventory)
class InventoryAdmin(BepAdminDefaults):
    list_display = ['_id', '_date', '_transcription', 'parish', 'print_source', '_books']
    search_fields = ['id', 'transcription']
    ordering = ['id']

    autocomplete_fields = ['manuscript_source', 'print_source', 'parish', 'monarch', 'injunction', 'books']
    inlines = [
        InventoryImageInline,
    ]

    @display(description="ID", ordering="id")
    def _id(self, obj):
        return f"{obj.id:05d}"

    @display(description="Transcription", ordering="transcription")
    def _transcription(self, obj):
        return f"{obj}"

    @display(description="Date", ordering="start_date")
    def _date(self, obj):
        if obj.start_date and obj.end_date:
            return f"{obj.start_date}-{obj.end_date}"
        elif obj.start_date:
            return f"{obj.start_date}"
        elif obj.end_date:
            return f"{obj.end_date}"
        return None

    @display(description="Books", ordering="books__count")
    def _books(self, obj):
        return obj.books.count()


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

    @display(description="ID", ordering="id")
    def _id(self, obj):
        return f"{obj.id:05d}"

    @display(description="Date")
    def _date(self, obj):
        if obj.written_date:
            return mark_safe(unescape(obj.written_date))
        if obj.start_date and obj.end_date:
            return f"{obj.start_date}-{obj.end_date}"
        elif obj.start_date:
            return f"{obj.start_date}"
        return 'No date'

    @display(description="Value", ordering=models.F('value').desc(nulls_last=True))
    def _value(self, obj):
        return Transaction.get_lsd_str(obj.value)

    @display(description="Books", ordering="books__count")
    def _books(self, obj):
        return obj.books.count()

    @display(description="Modern English", ordering="modern_transcription")
    def _modern_transcription(self, obj):
        return mark_safe(unescape(obj.modern_transcription))

@admin.register(Holding)
class HoldingAdmin(BepAdminDefaults):
    list_display = ['_date', 'parish', '_book']
    search_fields = ['start_date', 'end_date', 'written_date', 'description']
    ordering = ['start_date']
    autocomplete_fields = ['parish', 'archive', 'books']
    inlines = [
        HoldingImageInline,
    ]

    @display(description="Date & Source")
    def _date(self, obj):
        if obj.start_date and obj.end_date:
            return f"{obj.start_date}-{obj.end_date}"
        elif obj.start_date:
            return f"{obj.start_date}"
        elif obj.written_date:
            return obj.written_date
        return 'No date'

    @display(description="Modern English", ordering="modern_transcription")
    def _modern_transcription(self, obj):
        return mark_safe(unescape(obj.modern_transcription))

    @display(description="Book")
    def _book(self, obj):
        return mark_safe('<br>'.join(
            [str(n) for n in obj.books.all()]
        ))

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