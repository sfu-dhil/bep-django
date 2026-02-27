from django import forms
from django_select2.forms import Select2Widget

from .models import Transaction, Monarch, \
    Parish, Diocese, County, Book, \
    TransactionCategory, ManuscriptSource, PrintSource, Injunction

class TransactionAdminForm(forms.ModelForm):
    value_l = forms.IntegerField(min_value=0, initial=0, required=True, label="Cost in Pounds")
    value_s = forms.IntegerField(min_value=0, initial=0, required=True, label="Shillings")
    value_d = forms.IntegerField(min_value=0, initial=0, required=True, label="Pence")
    shipping_l = forms.IntegerField(min_value=0, initial=0, required=True, label="Carriage in Pounds")
    shipping_s = forms.IntegerField(min_value=0, initial=0, required=True, label="Shillings")
    shipping_d = forms.IntegerField(min_value=0, initial=0, required=True, label="Pence")

    class Meta:
        model = Transaction
        exclude = ['value', 'shipping']

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        initial = kwargs.get('initial', {})
        if instance:
            [l, s, d] = Transaction.get_lsd(instance.value)
            initial['value_l'] = l
            initial['value_s'] = s
            initial['value_d'] = d

            [l, s, d] = Transaction.get_lsd(instance.shipping)
            initial['shipping_l'] = l
            initial['shipping_s'] = s
            initial['shipping_d'] = d
        kwargs['initial'] = initial
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        transaction = super().save(commit=False)
        transaction.value = Transaction.get_total_from_lsd(self.cleaned_data['value_l'], self.cleaned_data['value_s'], self.cleaned_data['value_d'])
        transaction.shipping = Transaction.get_total_from_lsd(self.cleaned_data['shipping_l'], self.cleaned_data['shipping_s'], self.cleaned_data['shipping_d'])
        if commit:
            transaction.save(commit=True)
        return transaction

class TransactionSearchForm(forms.Form):
    q = forms.CharField(
        widget=forms.TextInput(attrs={
            'type': 'search',
            'placeholder': 'Search...',
            'class': 'form-control',
        }),
        required=False,
    )

    value_l_min = forms.IntegerField(min_value=0, required=False, label='Pounds')
    value_s_min = forms.IntegerField(min_value=0, required=False, label='Shillings')
    value_d_min = forms.IntegerField(min_value=0, required=False, label='Pence')
    value_l_max = forms.IntegerField(min_value=0, required=False, label='Pounds')
    value_s_max = forms.IntegerField(min_value=0, required=False, label='Shillings')
    value_d_max = forms.IntegerField(min_value=0, required=False, label='Pence')
    shipping_l_min = forms.IntegerField(min_value=0, required=False, label='Pounds')
    shipping_s_min = forms.IntegerField(min_value=0, required=False, label='Shillings')
    shipping_d_min = forms.IntegerField(min_value=0, required=False, label='Pence')
    shipping_l_max = forms.IntegerField(min_value=0, required=False, label='Pounds')
    shipping_s_max = forms.IntegerField(min_value=0, required=False, label='Shillings')
    shipping_d_max = forms.IntegerField(min_value=0, required=False, label='Pence')
    year_min = forms.IntegerField(min_value=0, required=False)
    year_max = forms.IntegerField(min_value=0, required=False)
    transaction_category = forms.ModelChoiceField(
        widget=Select2Widget(attrs={
            'data-theme': 'bootstrap-5',
        }),
        queryset=TransactionCategory.objects.order_by('label').all(),
        required=False,
    )
    monarch = forms.ModelChoiceField(
        widget=Select2Widget(attrs={
            'data-theme': 'bootstrap-5',
        }),
        queryset=Monarch.objects.order_by('start_date', 'label').all(),
        required=False,
    )
    diocese = forms.ModelChoiceField(
        widget=Select2Widget(attrs={
            'data-theme': 'bootstrap-5',
        }),
        queryset=Diocese.objects.order_by('label').all(),
        required=False,
    )
    county = forms.ModelChoiceField(
        widget=Select2Widget(attrs={
            'data-theme': 'bootstrap-5',
        }),
        queryset=County.objects.order_by('label').all(),
        required=False,
    )
    parish = forms.ModelChoiceField(
        widget=Select2Widget(attrs={
            'data-theme': 'bootstrap-5',
        }),
        queryset=Parish.objects.order_by('label').all(),
        required=False,
    )
    book = forms.ModelChoiceField(
        widget=Select2Widget(attrs={
            'data-theme': 'bootstrap-5',
        }),
        queryset=Book.objects.order_by('title').all(),
        required=False,
    )
    manuscript_source = forms.ModelChoiceField(
        widget=Select2Widget(attrs={
            'data-theme': 'bootstrap-5',
        }),
        queryset=ManuscriptSource.objects.order_by('label').all(),
        required=False,
    )
    print_source = forms.ModelChoiceField(
        widget=Select2Widget(attrs={
            'data-theme': 'bootstrap-5',
        }),
        queryset=PrintSource.objects.order_by('title').all(),
        required=False,
    )
    injunction = forms.ModelChoiceField(
        widget=Select2Widget(attrs={
            'data-theme': 'bootstrap-5',
        }),
        queryset=Injunction.objects.order_by('title').all(),
        required=False,
    )

class ParishSearchForm(forms.Form):
    q = forms.CharField(
        widget=forms.TextInput(attrs={
            'type': 'search',
            'placeholder': 'Search...',
            'class': 'form-control',
        }),
        required=False,
    )

    diocese = forms.ModelChoiceField(
        widget=Select2Widget(attrs={
            'data-theme': 'bootstrap-5',
        }),
        queryset=Diocese.objects.order_by('label').all(),
        required=False,
    )
    county = forms.ModelChoiceField(
        widget=Select2Widget(attrs={
            'data-theme': 'bootstrap-5',
        }),
        queryset=County.objects.order_by('label').all(),
        required=False,
    )

class DioceseSearchForm(forms.Form):
    q = forms.CharField(
        widget=forms.TextInput(attrs={
            'type': 'search',
            'placeholder': 'Search...',
            'class': 'form-control',
        }),
        required=False,
    )

class CountySearchForm(forms.Form):
    q = forms.CharField(
        widget=forms.TextInput(attrs={
            'type': 'search',
            'placeholder': 'Search...',
            'class': 'form-control',
        }),
        required=False,
    )