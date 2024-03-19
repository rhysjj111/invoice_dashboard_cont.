from django import forms
from .models import Customer
from crispy_bootstrap5.bootstrap5 import FloatingField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Row, Column
from crispy_forms.bootstrap import FormActions


class CustomerForm(forms.ModelForm):
    name = forms.CharField(
        label = "Full name/Company name"
    )
    friendly_name = forms.CharField(
        label = "Screen name",
        required = False
    )
    contact_number_primary = forms.CharField(
        label = "Primary contact number",
        required = False
    )
    city_region = forms.CharField(
        label = "Town/city",
        required = False
    )

    class Meta:
        model  = Customer
        fields = ('name', 'friendly_name', 'email', 'contact_number_primary',
                  'postcode', 'city_region', 'address_line_1', 'address_line_2',
                  'payment_terms')
        
        

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_action = 'add/'
        self.helper.layout = Layout(
            Row(
                Column(
                    FloatingField(
                        'name', 'friendly_name', 'email', 'contact_number_primary', 'payment_terms'
                        )
                ),
                Column(
                    FloatingField(
                        'address_line_1', 'address_line_2', 'city_region', 'postcode'
                        ),
                    
                )
                ),FormActions(
                    Submit(
                        'submit',
                        'Add customer',
                        css_class='float-end')))