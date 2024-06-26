from django import forms
from django.forms.widgets import Select, DateInput
from django.shortcuts import reverse
from .models import Invoice, Part, Labour, Customer, Vehicle
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Reset, Field, ButtonHolder, HTML
from crispy_forms.bootstrap import Modal, UneditableField
from crispy_bootstrap5.bootstrap5 import FloatingField
from django.forms import inlineformset_factory, BaseInlineFormSet


def add_or_edit_modal(slug, type, layout):
    if slug:
        layout
    else:
        layout = Modal(
            layout,
            Row(
                Column(
                    ButtonHolder(
                        Submit(
                            'submit',
                            'Save',
                            css_class='float-end'
                        ),css_class='',
                    )
                )
            ),
            css_id=type+"_modal",
            title="Add "+type.capitalize(),
            css_class="modal-lg h-100 overflow-y-auto"
        )
    return  layout
      

class CustomSelectWidget(Select):
    """ 
    Custom select widget with purpose of updating each vehicle 
    choice class with it's corrsponding customer fk.
    (To assist with Javascript function which only shows 
    relevant vehicle choices for the customer selected 
    when creating an invoice.)
    """
    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option = super().create_option(
            name, value, label, selected, index, subindex=subindex, attrs=attrs)
        try:
            instance = self.choices.queryset.get(pk=value.value)
            option_fk = instance.customer.id
            if option_fk:
                option['attrs']['class'] = option_fk
        except:
            option['attrs']['class'] = 'no_customer'
        return option


class InvoiceForm(forms.ModelForm):

    vehicle = forms.ModelChoiceField(
        queryset=Vehicle.objects.all(), widget=CustomSelectWidget)
    
    date_in = forms.DateField(
        label="From Date", widget=DateInput(attrs={'type': 'date'}))

    class Meta:
        model  = Invoice
        fields = ('customer', 'vehicle', 'date_in', 'mileage','status')
        

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.required = False
        
        slug = self.instance.slug

        self.helper = FormHelper()
        self.helper.form_action = 'None' if slug else reverse('create_invoice')
        if slug:
            self.helper.form_tag = False
            self.helper.disable_csrf = True
        self.helper.layout = add_or_edit_modal(
            slug,
            'invoice',
            Layout(
                Row(
                    Field('status', type="hidden"), css_class='mb-3'
                ),
                Row(
                    Column(
                        FloatingField('customer', 'date_in')
                    ),
                    Column(
                        FloatingField(
                            'vehicle', 'mileage'
                        )
                    ),
                )                       
            )
        )   


class PositiveIntegerField(forms.IntegerField):
    def clean(self, value):
        value = super().clean(value)
        if value is not None:
            if value < 0:
                raise forms.ValidationError("This field must be a positive integer.")
        return value


class PositiveDecimalField(forms.DecimalField):
    def clean(self, value):
        value = super().clean(value)
        if value is not None:
            if value < 0:
                raise forms.ValidationError("This field must be a positive decimal.")
        return value


class PartForm(forms.ModelForm):

    cost_to_company = PositiveDecimalField(
        label="Cost", max_digits=10, decimal_places=2)
    price_to_customer = PositiveDecimalField(
        label="Price", max_digits=10, decimal_places=2)
    quantity = PositiveIntegerField(label='Qty')

    class Meta:
        model  = Part
        fields = ('cost_to_company', 'price_to_customer', 
                  'title','quantity')   

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.required = False

        # Convert pence to pounds (formatted to 2dp)
        for entry in ['cost_to_company', 'price_to_customer']:
            price_sub_unit = self.initial.get(entry)
            if price_sub_unit is not None:
                price_unit = round((price_sub_unit / 100), 2)
                self.initial[entry] = "{:.2f}".format(price_unit)


    def save(self, commit=True):
        # Convert pounds to pence
        for entry in ['cost_to_company', 'price_to_customer']:
            price_unit = self.cleaned_data.get(entry)
            if price_unit is not None:
                price_sub_unit = price_unit * 100
                setattr(self.instance, entry, price_sub_unit)

        if commit:
            self.instance.save()
        return self.instance


class BasePartFormSet(BaseInlineFormSet):

    def __init__(self, *args, **kwargs):
        super(BasePartFormSet, self).__init__(*args, **kwargs)
        self.can_delete = True
        self.extra=1

    def clean(self):
        super().clean()
        # deletes form with no input values 
        empty_forms = []               
        for form in self.forms:
            if self._is_form_empty(form):
                empty_forms.append(form)
        for form in empty_forms:
            self.forms.remove(form)
    
    def _is_form_empty(self, form):
        """Function to check all input values in form are empty"""
        for field_name, value in form.cleaned_data.items():
            if value is not None and value != '':
                return False
        return True


class BasePartFormSetHelper(FormHelper):

    def __init__(self, *args, **kwargs):
        super(BasePartFormSetHelper, self).__init__(*args, **kwargs)
        self.form_tag = False
        self.disable_csrf = True
        self.layout = Layout(
            Row(
                Column(
                    FloatingField('title')
                ),
                Column(
                    FloatingField('cost_to_company')
                ),
                Column(
                    FloatingField('price_to_customer')
                ),
                Column(
                    Row(
                        Column(FloatingField('quantity'), css_class='w-50'),
                        Column(Field('DELETE'), css_class='w-50'),
                        css_class='align-items-center'
                    )                    
                )
            )
        )

PartFormSet = inlineformset_factory(
    parent_model=Invoice,
    model=Part,
    form=PartForm,
    formset=BasePartFormSet,
    can_delete=True)


class LabourForm(forms.ModelForm):

    description = forms.CharField(
        widget=forms.Textarea())
    hours = PositiveDecimalField(
        label='Hrs', max_digits=4, decimal_places=2)

    class Meta:
        model  = Labour
        fields = ('hours', 'description')   

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.required = False


class BaseLabourFormSet(BaseInlineFormSet):

    def __init__(self, *args, **kwargs):
        super(BaseLabourFormSet, self).__init__(*args, **kwargs)
        self.can_delete = True
        self.extra=1

    def clean(self):
        super().clean()
        # deletes form with no input values 
        empty_forms = []               
        for form in self.forms:
            if self._is_form_empty(form):
                empty_forms.append(form)
        for form in empty_forms:
            self.forms.remove(form)
    
    def _is_form_empty(self, form):
        """Function to check all input values in form are empty"""
        for field_name, value in form.cleaned_data.items():
            if value is not None and value != '':
                return False
        return True


class BaseLabourFormSetHelper(FormHelper):

    def __init__(self, *args, **kwargs):
        super(BaseLabourFormSetHelper, self).__init__(*args, **kwargs)

        self.form_tag = False
        self.disable_csrf = True
        self.layout = Layout(
            Row(  
                Column(FloatingField('description', css_class='desc_text_area col-10')),
                Column(
                    Row(
                        Column(FloatingField('hours'))
                        
                    ),
                    Row(

                        Column(Field('DELETE') )                          
                    ),
                    css_class='col-2'
                )         
            )
        )

LabourFormSet = inlineformset_factory(
    parent_model=Invoice,
    model=Labour,
    form=LabourForm,
    formset=BaseLabourFormSet,
    can_delete=True)


