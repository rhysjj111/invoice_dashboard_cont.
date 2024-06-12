from django import forms
from django.shortcuts import reverse
from .models import Customer, Vehicle
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Reset, Field, ButtonHolder, HTML
from crispy_forms.bootstrap import Modal, PrependedText
from crispy_bootstrap5.bootstrap5 import FloatingField

def add_or_edit_button(slug):
    if slug:
        text = 'Edit'
    else:
        text = 'Add'
    return text

def add_or_edit_trash(slug):
    if slug:
        return HTML('<button type="button" data-bs-toggle="modal" data-bs-target='
                    f'"#delete-{slug}-modal" class="ms-4 btn btn-light p-2 rounded-4">'
                    '<i class="bi-trash icon text-danger fs-3 align-middle"></i></button>')

def add_or_edit_path(slug, type):
    if slug:
        path = reverse('edit_'+type, args=[slug])
    else:
        path = reverse('add_'+type)
    return path

def add_or_edit_modal(slug, type, layout):
    if slug:
        layout
    else:
        layout = Modal(
            layout,
            css_id=type+"_modal",
            title="Add "+type.capitalize(),
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
        self.helper.form_action = add_or_edit_path(self.instance.slug, 'customer')
        self.helper.form_class = 'mb-3'
        self.helper.layout = add_or_edit_modal(
            self.instance.slug,
            'customer',
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
                    ),
                ),
                Row(
                    Column(
                        ButtonHolder(
                            Submit(
                                'submit',
                                'Save',
                                css_class='ms-2'
                            )
                        )
                    )
                )
            ) 
        )   


class VehicleForm(forms.ModelForm):


    class Meta:
        model  = Vehicle
        fields = ('customer', 'registration', 'make', 'model')


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_action = add_or_edit_path(self.instance.slug, 'vehicle')
        self.helper.form_class = 'mb-3'
        self.helper.layout = add_or_edit_modal(
            self.instance.slug,
            'vehicle',
            Layout(
                Row(
                    Field('customer', type="hidden"), css_class='mb-3'
                ),
                Row(
                    Column(
                        FloatingField(
                            'registration'
                        ) 
                    ),
                    Column(
                        FloatingField(
                            'make'
                        ) 
                    ),
                    Column(
                        FloatingField(
                            'model'
                        )
                    ),
                    Column(
                        ButtonHolder(                            
                            Submit(
                                'submit',
                                'Save',
                                css_class='ms-2'                         
                            ),
                            add_or_edit_trash(self.instance.slug)
                        )
                    ), css_class='d-flex align-items-center'                  
                )
            ) 
        )   


    
