from django.db import models
from django_advance_thumbnail import AdvanceThumbnailField
from django.contrib.postgres.fields import ArrayField
from django.utils.html import strip_tags
from django.utils.safestring import mark_safe
from html import unescape
from math import floor

# abstract Models
class AbstractImage(models.Model):
    image = models.ImageField(
        max_length=None,
        upload_to='images/',
        help_text=mark_safe('Please use <a class="text-primary-500" href="https://developer.mozilla.org/en-US/docs/Web/Media/Formats/Image_types" target="_blank">standard web image types</a>. PNG, JPEG, and WebP are recommended.'),
        width_field='image_width',
        height_field='image_height',
    )
    image_width = models.IntegerField(null=True, blank=True)
    image_height = models.IntegerField(null=True, blank=True)

    thumbnail = AdvanceThumbnailField(
        max_length=None,
        source_field='image',
        upload_to='thumbnails/',
        null=True,
        blank=True,
        size=(520, 520),
    )

    description = models.TextField(blank=True)
    license = models.TextField(blank=True)

    class Meta:
        abstract = True

# Models (load order matters)
class Nation(models.Model):
    label = models.CharField(unique=True)
    description = models.TextField(blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # relationships

    # one-to-many provinces via Province Model
    # one-to-many counties via County Model
    # one-to-many injunctions via Injunction Model

    class Meta:
        db_table = 'bep_nation'

    def __str__(self):
        return mark_safe(f"{self.label}")

class Archive(models.Model):
    label = models.CharField(unique=True)
    description = models.TextField(blank=True)
    links = ArrayField(models.URLField(max_length=None), blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # relationships

    # one-to-many manuscript_sources via ManuscriptSource Model
    # one-to-many holdings via Holding Model

    class Meta:
        db_table = 'bep_archive'

    def __str__(self):
        return mark_safe(f"{self.label}")

class TransactionCategory(models.Model):
    label = models.CharField(unique=True)
    description = models.TextField(blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # relationships

    # many-to-many transactions via Transaction Model

    class Meta:
        db_table = 'bep_transaction_category'
        verbose_name_plural = 'transaction categories'

    def __str__(self):
        return mark_safe(f"{self.label}")

class SourceCategory(models.Model):
    label = models.CharField(unique=True)
    description = models.TextField(blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # relationships

    # one-to-many manuscript_sources via ManuscriptSource Model
    # one-to-many print_sources via PrintSource Model

    class Meta:
        db_table = 'bep_source_category'
        verbose_name_plural = 'source categories'

    def __str__(self):
        return mark_safe(f"{self.label}")

class Monarch(models.Model):
    label = models.CharField(unique=True)
    description = models.TextField(blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # relationships

    # one-to-many transactions via Transaction Model
    # one-to-many injunctions via Injunction Model
    # one-to-many inventories via Inventory Model
    # one-to-many books via Book Model

    class Meta:
        db_table = 'bep_monarch'

    def __str__(self):
        return mark_safe(f"{self.label} ({self.start_date} - {self.end_date})" if self.start_date and self.end_date else f"{self.label}")

class Format(models.Model):
    label = models.CharField(unique=True)
    description = models.TextField(blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # relationships

    # one-to-many books via Book Model

    class Meta:
        db_table = 'bep_format'

    def __str__(self):
        return mark_safe(f"{self.label}")


class County(models.Model):
    label = models.CharField(unique=True)
    description = models.TextField(blank=True)
    links = ArrayField(models.URLField(max_length=None), blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # relationships
    nation = models.ForeignKey(
        Nation,
        related_name='counties',
        on_delete=models.CASCADE,
    )

    # one-to-many towns via Town Model

    class Meta:
        db_table = 'bep_county'
        verbose_name_plural = 'counties'

    def __str__(self):
        return mark_safe(f"{self.label}")


class Province(models.Model):
    label = models.CharField(unique=True)
    description = models.TextField(blank=True)
    links = ArrayField(models.URLField(max_length=None), blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # relationships
    nation = models.ForeignKey(
        Nation,
        related_name='provinces',
        on_delete=models.CASCADE,
    )

    # one-to-many dioceses via Diocese Model
    # one-to-many injunctions via Injunction Model

    class Meta:
        db_table = 'bep_province'

    def __str__(self):
        return mark_safe(f"{self.label}")

class Town(models.Model):
    label = models.CharField(unique=True)
    description = models.TextField(blank=True)
    in_london = models.BooleanField()
    links = ArrayField(models.URLField(max_length=None), blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # relationships
    county = models.ForeignKey(
        County,
        related_name='towns',
        on_delete=models.CASCADE,
    )

    # one-to-many parishes via Parish Model

    class Meta:
        db_table = 'bep_town'

    def __str__(self):
        return mark_safe(f"{self.label}")


class Diocese(models.Model):
    label = models.CharField(unique=True)
    description = models.TextField(blank=True)
    links = ArrayField(models.URLField(max_length=None), blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # relationships
    province = models.ForeignKey(
        Province,
        related_name='dioceses',
        on_delete=models.CASCADE,
    )

    # one-to-many archdeaconries via Archdeaconry Model
    # one-to-many injunctions via Injunction Model

    class Meta:
        db_table = 'bep_diocese'

    def __str__(self):
        return mark_safe(f"{self.label}")

class Archdeaconry(models.Model):
    label = models.CharField(unique=True)
    description = models.TextField(blank=True)
    links = ArrayField(models.URLField(max_length=None), blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # relationships
    diocese = models.ForeignKey(
        Diocese,
        related_name='archdeaconries',
        on_delete=models.CASCADE
    )
    # one-to-many parishes via Parish Model
    # one-to-many injunctions via Injunction Model

    class Meta:
        db_table = 'bep_archdeaconry'
        verbose_name_plural = 'archdeaconries and courts'

    def __str__(self):
        return mark_safe(f"{self.label}")


class Parish(models.Model):
    label = models.CharField(unique=True)
    description = models.TextField(blank=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    address = models.TextField(blank=True)
    links = ArrayField(models.URLField(max_length=None), blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # relationships
    archdeaconry = models.ForeignKey(
        Archdeaconry,
        related_name='parishes',
        on_delete=models.CASCADE,
    )
    town = models.ForeignKey(
        Town,
        null=True,
        blank=True,
        related_name='parishes',
        on_delete=models.SET_NULL,
    )

    # one-to-many transactions via Transaction Model
    # one-to-many inventories via Inventory Model
    # one-to-many holdings via Holding Model

    class Meta:
        db_table = 'bep_parish'
        verbose_name_plural = "parishes"

    def __str__(self):
        return mark_safe(f"{self.label}")

class PrintSource(models.Model):
    title = models.CharField()
    author = models.CharField(blank=True)
    date = models.CharField(blank=True)
    publisher = models.CharField(blank=True)
    notes = models.TextField(blank=True)
    links = ArrayField(models.URLField(max_length=None), blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # relationships
    source_category = models.ForeignKey(
        SourceCategory,
        related_name='print_sources',
        on_delete=models.CASCADE,
    )

    # one-to-many transactions via Transaction Model
    # one-to-many inventories via Inventory Model

    class Meta:
        db_table = 'bep_print_source'

    def __str__(self):
        return mark_safe(f"{self.title}")

class ManuscriptSource(models.Model):
    call_number = models.CharField(blank=True)
    label = models.CharField(unique=True)
    description = models.TextField(blank=True)
    links = ArrayField(models.URLField(max_length=None), blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # relationships
    source_category = models.ForeignKey(
        SourceCategory,
        related_name='manuscript_sources',
        on_delete=models.CASCADE,
    )
    archive = models.ForeignKey(
        Archive,
        related_name='manuscript_sources',
        on_delete=models.CASCADE,
    )

    # one-to-many transactions via Transaction Model
    # one-to-many inventories via Inventory Model

    class Meta:
        db_table = 'bep_manuscript_source'

    def __str__(self):
        return mark_safe(f"{self.label}")

class Book(models.Model):
    title = models.CharField(blank=True)
    uniform_title = models.CharField(blank=True)
    variant_titles = ArrayField(models.CharField(), blank=True)
    author = models.CharField(blank=True)
    imprint = models.TextField(blank=True)
    variant_imprint = models.TextField(blank=True, verbose_name="Imprint, Modern English")
    date = models.CharField(blank=True)
    estc = models.CharField(blank=True)
    physical_description = models.TextField(blank=True)
    description = models.TextField(blank=True)
    notes = models.TextField(blank=True, verbose_name="Private Notes")
    links = ArrayField(models.URLField(max_length=None), blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # relationships
    format = models.ForeignKey(
        Format,
        null=True,
        blank=True,
        related_name='books',
        on_delete=models.SET_NULL,
    )
    monarch = models.ForeignKey(
        Monarch,
        null=True,
        blank=True,
        related_name='books',
        on_delete=models.SET_NULL,
    )

    # many-to-many transactions via Transaction Model
    # many-to-many inventories via Inventory Model
    # many-to-many holdings via Holding Model

    class Meta:
        db_table = 'bep_book'

    def __str__(self):
        if self.uniform_title:
            return mark_safe(self.uniform_title)
        elif self.title:
            return mark_safe(self.title)
        elif self.description:
            return mark_safe(self.description)
        return 'No description provided'

class Holding(models.Model):
    description = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    written_date = models.CharField(blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # relationships
    parish = models.ForeignKey(
        Parish,
        related_name='holdings',
        on_delete=models.CASCADE,
    )
    archive = models.ForeignKey(
        Archive,
        null=True,
        blank=True,
        related_name='holdings',
        on_delete=models.SET_NULL,
    )
    books = models.ManyToManyField(
        Book,
        blank=True,
        related_name='holdings',
    )

    # one-to-many images via HoldingImage Model

    class Meta:
        db_table = 'bep_holding'
        verbose_name = 'surviving text'

    def __str__(self):
        return ', '.join(
            [str(n) for n in self.books.all()]
        ) + f"{self.parish}"

class HoldingImage(AbstractImage):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # relationships
    holding = models.ForeignKey(
        Holding,
        null=True,
        blank=True,
        related_name='images',
        on_delete=models.CASCADE,
    )

    class Meta:
        db_table = 'bep_holding_image'
        verbose_name = 'surviving text image'

    def __str__(self):
        return self.image.name if self.image else self.id

class Injunction(models.Model):
    title = models.CharField()
    uniform_title = models.CharField(blank=True)
    variant_titles = ArrayField(models.CharField(), blank=True)
    author = models.CharField(blank=True)
    imprint = models.TextField(blank=True)
    variant_imprint = models.TextField(blank=True, verbose_name="Imprint, Modern English")
    estc = models.CharField(blank=True)
    date = models.CharField(blank=True)
    physical_description = models.TextField(blank=True)
    transcription = models.TextField(blank=True)
    modern_transcription = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    links = ArrayField(models.URLField(max_length=None), blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # relationships
    nation = models.ForeignKey(
        Nation,
        null=True,
        blank=True,
        related_name='injunctions',
        on_delete=models.SET_NULL,
    )
    diocese = models.ForeignKey(
        Diocese,
        null=True,
        blank=True,
        related_name='injunctions',
        on_delete=models.SET_NULL,
    )
    province = models.ForeignKey(
        Province,
        null=True,
        blank=True,
        related_name='injunctions',
        on_delete=models.SET_NULL,
    )
    archdeaconry = models.ForeignKey(
        Archdeaconry,
        null=True,
        blank=True,
        related_name='injunctions',
        on_delete=models.SET_NULL,
    )
    monarch = models.ForeignKey(
        Monarch,
        null=True,
        blank=True,
        related_name='injunctions',
        on_delete=models.SET_NULL,
    )

    # one-to-many transactions via Transaction Model
    # one-to-many inventories via Inventory Model

    class Meta:
        db_table = 'bep_injunction'

    def __str__(self):
        return mark_safe(f"{self.title}")

class Inventory(models.Model):
    page_number = models.CharField(blank=True)
    transcription = models.TextField()
    modifications = models.TextField()
    description = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    written_date = models.CharField(blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # relationships
    manuscript_source = models.ForeignKey(
        ManuscriptSource,
        null=True,
        blank=True,
        related_name='inventories',
        on_delete=models.SET_NULL,
    )
    print_source = models.ForeignKey(
        PrintSource,
        null=True,
        blank=True,
        related_name='inventories',
        on_delete=models.SET_NULL,
    )
    parish = models.ForeignKey(
        Parish,
        related_name='inventories',
        on_delete=models.CASCADE,
    )
    monarch = models.ForeignKey(
        Monarch,
        null=True,
        blank=True,
        related_name='inventories',
        on_delete=models.SET_NULL,
    )
    injunction = models.ForeignKey(
        Injunction,
        null=True,
        blank=True,
        related_name='inventories',
        on_delete=models.SET_NULL,
    )
    books = models.ManyToManyField(
        Book,
        blank=True,
        related_name='inventories',
    )

    # one-to-many images via InventoryImage Model

    class Meta:
        db_table = 'bep_inventory'
        verbose_name_plural = 'inventories'

    def __str__(self):
        str = strip_tags(unescape(self.transcription))
        return f"{str[:100]}..." if len(str) > 103 else str


class InventoryImage(AbstractImage):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # relationships
    inventory = models.ForeignKey(
        Inventory,
        null=True,
        blank=True,
        related_name='images',
        on_delete=models.CASCADE,
    )

    class Meta:
        db_table = 'bep_inventory_image'

    def __str__(self):
        return self.image.name if self.image else self.id


class Transaction(models.Model):
    value = models.IntegerField(null=True, blank=True)
    shipping = models.IntegerField(null=True, blank=True)
    copies = models.IntegerField(null=True, blank=True)
    location = models.CharField(blank=True)
    page = models.CharField(blank=True)
    transcription = models.TextField(blank=True)
    modern_transcription = models.TextField(blank=True, verbose_name="Modern English")
    public_notes = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    written_date = models.CharField(blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # relationships
    parish = models.ForeignKey(
        Parish,
        related_name='transactions',
        on_delete=models.CASCADE,
    )
    manuscript_source = models.ForeignKey(
        ManuscriptSource,
        null=True,
        blank=True,
        related_name='transactions',
        on_delete=models.SET_NULL,
    )
    print_source = models.ForeignKey(
        PrintSource,
        null=True,
        blank=True,
        related_name='transactions',
        on_delete=models.SET_NULL,
    )
    injunction = models.ForeignKey(
        Injunction,
        null=True,
        blank=True,
        related_name='transactions',
        on_delete=models.SET_NULL,
    )
    monarch = models.ForeignKey(
        Monarch,
        null=True,
        blank=True,
        related_name='transactions',
        on_delete=models.SET_NULL,
    )

    transaction_categories = models.ManyToManyField(
        TransactionCategory,
        blank=True,
        related_name='transactions',
    )
    books = models.ManyToManyField(
        Book,
        blank=True,
        related_name='transactions',
    )

    class Meta:
        db_table = 'bep_transaction'

    def __str__(self):
        return f"{self.id:05d}"

    @staticmethod
    def get_lsd(total_pence):
        if total_pence == None:
            total_pence = 0
        elif isinstance(total_pence, str):
            total_pence = int(total_pence) if total_pence.isdigit() else 0

        l = floor(total_pence/ 240)
        s = floor((total_pence % 240) / 12)
        d = (total_pence % 240) % 12
        return [l, s, d]

    @staticmethod
    def get_lsd_str(total_pence):
        l, s, d = Transaction.get_lsd(total_pence)
        return f"£{l}. {s}s. {d}d"