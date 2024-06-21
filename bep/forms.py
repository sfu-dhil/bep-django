from django import forms
from unfold.widgets import UnfoldAdminIntegerFieldWidget

from .models import Transaction

class TransactionAdminForm(forms.ModelForm):
    value_l = forms.IntegerField(min_value=0, initial=0, required=True, widget=UnfoldAdminIntegerFieldWidget, label="Cost in Pounds")
    value_s = forms.IntegerField(min_value=0, initial=0, required=True, widget=UnfoldAdminIntegerFieldWidget, label="Shillings")
    value_d = forms.IntegerField(min_value=0, initial=0, required=True, widget=UnfoldAdminIntegerFieldWidget, label="Pence")
    shipping_l = forms.IntegerField(min_value=0, initial=0, required=True, widget=UnfoldAdminIntegerFieldWidget, label="Carriage in Pounds")
    shipping_s = forms.IntegerField(min_value=0, initial=0, required=True, widget=UnfoldAdminIntegerFieldWidget, label="Shillings")
    shipping_d = forms.IntegerField(min_value=0, initial=0, required=True, widget=UnfoldAdminIntegerFieldWidget, label="Pence")

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
        transaction.value = 240 * self.cleaned_data['value_l'] + 12 * self.cleaned_data['value_s'] + self.cleaned_data['value_d']
        transaction.shipping = 240 * self.cleaned_data['shipping_l']  + 12 * self.cleaned_data['shipping_s'] + self.cleaned_data['shipping_d']
        if commit:
            transaction.save(commit=True)
        return transaction