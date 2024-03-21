from django import forms
from django.shortcuts import reverse
from .models import Customer
from crispy_bootstrap5.bootstrap5 import FloatingField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Row, Column, ButtonHolder, Reset
from crispy_forms.bootstrap import FormActions, Modal

def add_or_edit_path(slug):
    if slug:
        path = reverse('edit_customer', args=[slug])
    else:
        path = reverse('add_customer')
    return path

def add_or_edit_modal(instance, layout):
    if instance:
        layout
    else:
        layout = Modal(
            layout,
            css_id="customer_modal",
            title="Add Customer",
            css_class="modal-lg h-100 overflow-y-auto"
        )
    return  layout  
        


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
        fields = ('name', 'friendly_name', 'type', 'email', 'contact_number_primary',
                  'postcode', 'city_region', 'address_line_1', 'address_line_2',
                  'payment_terms')
        

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_action = add_or_edit_path(self.instance.slug)
        self.helper.form_class = 'mb-4'

        self.helper.layout = add_or_edit_modal(
            self.instance.slug,
            Layout(
                Row(
                    Column(
                        FloatingField(
                            'name', 'friendly_name', 'email', 'contact_number_primary', 'type'
                        )
                    ),
                    Column(
                        FloatingField(
                            'address_line_1', 'address_line_2', 'city_region', 'postcode', 'payment_terms'
                        ),
                    )
                ),
                Row(
                    Column(
                        ButtonHolder(
                            Reset(
                                'reset-form',
                                'Reset'
                            ),
                            Submit(
                                'submit',
                                'Add customer',
                                css_class='ms-4'
                            ),
                            css_class='float-end'
                        )
                    )
                )
            ) 
        )   
