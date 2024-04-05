from django.db import models
from django.db.models import Sum
from django.conf import settings
from django.utils.text import slugify
from customer.models import Customer, Vehicle
from django.utils import timezone
from uuid import uuid4
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.validators import validate_email


class Invoice(models.Model):

    class InvoiceStatus(models.IntegerChoices):
        WORK_ON_HOLD = 1, 'Work on hold'
        OPEN = 2, 'Open'
        READY_FOR_PROCESSING = 3, 'Ready for processing'
        READY_FOR_VERIFICATION = 4, 'Ready for verification'
        SENT_TO_CUSTOMER = 5, 'Sent to customer'
        COMPLETE = 6, 'Complete'

    inv_number = models.CharField(
        max_length=10, null=True, editable=False)
    inv_integer = models.PositiveIntegerField(null=True, editable=False)
    customer = models.ForeignKey(
        Customer, on_delete=models.PROTECT, related_name='invoices', 
        blank=True, null=True)
    vehicle = models.ForeignKey(
        Vehicle, on_delete=models.PROTECT, related_name='invoices', 
        blank=True, null=True)
    date_in = models.DateTimeField(blank=True, null=True)
    mileage = models.PositiveIntegerField(blank=True, null=True)
    status = models.PositiveSmallIntegerField(
        choices=InvoiceStatus.choices, blank=True, null=True)
    active = models.BooleanField(default=True, blank=True, null=True)
    parts_total = models.PositiveIntegerField(blank=True, null=True)
    labour_total = models.PositiveIntegerField(blank=True, null=True)
    subtotal = models.PositiveIntegerField(blank=True, null=True)
    vat_total = models.PositiveIntegerField(blank=True, null=True)
    grand_total = models.PositiveIntegerField(blank=True, null=True)

    # utilities
    slug = models.SlugField(max_length=100, unique=True, blank=False, null=False)
    unique_id = models.CharField(null=True, blank=True, max_length=100)   

    def __str__(self):
        if self.inv_integer:
            result = f'{self.customer} - {self.vehicle} - {self.inv_number}'
        elif self.customer and self.vehicle:
            result = f'{self.customer} - {self.vehicle} - ({self.unique_id})'
        elif self.customer or self.vehicle:
            result = f'{self.customer or self.vehicle} - ({self.unique_id})'
        else:
            result = f'Blank invoice - ({self.unique_id})'
        return result

    def update_total(self):
        #update grand_total each time a part or labour entry is updated.

        #check no parts or labour total fields equal None
        parts_total_none = any(part.total is None for part in self.parts.all())
        labour_total_none = any(labour.total is None for labour in self.labour.all())

        if not parts_total_none and not labour_total_none:     
            parts_total = self.parts.aggregate(Sum('total'))['total__sum']
            labour_total = self.labour.aggregate(Sum('total'))['total__sum']

            self.parts_total = parts_total or 0
            self.labour_total = labour_total or 0
            self.subtotal = self.parts_total + self.labour_total

            if self.subtotal > 0:
                self.vat_total = self.subtotal * settings.VAT_PERCENTAGE
                self.grand_total = self.subtotal + self.vat_total
            else:
                self.grand_total = 0
                self.vat_total = 0
        else:
            self.grand_total = self.vat_total = self.subtotal = 0
        self.save()


    def save(self, *args, **kwargs):
        # create a todays date if no date provided
        if self.date_in is None:
            self.date_in = timezone.localtime(timezone.now())

        # Set active to True or False and create invoice number depending on invoice status.
        if self.status:
            if self.status == 5:
                # Check if the customer has an email address
                if not self.customer.email:
                    raise ValidationError("Customer must have an email address.")
                
                # Check email is valid
                try:
                    validate_email(self.customer.email)
                except ValidationError as e:
                    raise ValueError("Invalid email address: {}".format(e))

                # Check if all required fields are filled in
                if not all([self.customer, self.vehicle, self.date_in, 
                            self.mileage]):
                    raise ValidationError("All invoice details must be filled in.")

                # Check if grand_total is greater than 0
                if self.grand_total is not None and self.grand_total <= 0:
                    raise ValidationError("Grand total must be greater than 0.")

                self.active = False 

                if self.inv_number is None:
                    try:
                        latest = Invoice.objects.filter(inv_integer__gt=0).latest('inv_integer')
                        latest = latest.inv_integer
                    except Invoice.DoesNotExist:
                        latest = 0                    
                    self.inv_integer = latest + 1
                    self.inv_number = f'INV_#{self.inv_integer}'
            else:
                self.active = True
        
        if self.unique_id is None:
            self.unique_id = str(uuid4()).split('-')[4]
                   
        self.slug = slugify(f'{self.unique_id}')

        super().save(*args, **kwargs)


class Part(models.Model):

    invoice = models.ForeignKey(
        Invoice, on_delete=models.PROTECT, related_name='parts')
    cost_to_company = models.PositiveIntegerField( null=True, blank=True)
    price_to_customer = models.PositiveIntegerField(null=True, blank=True)
    title = models.CharField(max_length=25, null=False, blank=False)
    quantity = models.PositiveIntegerField( null=True, blank=True)
    total = models.PositiveIntegerField(null=True, blank=True)

    def save(self, *args, **kwargs):
        """update part subtotal on save"""
        if all([self.price_to_customer, self.cost_to_company, self.title, self.quantity]): 
            self.total = self.price_to_customer * self.quantity
        else:
            self.total = None
        super().save(*args, **kwargs)


class Labour(models.Model):

    class Meta:
        verbose_name_plural = 'Labour'

    invoice = models.ForeignKey(
        Invoice, on_delete=models.PROTECT, related_name='labour')
    description = models.CharField(max_length=250, null=True, blank=True)
    hours = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    total = models.PositiveIntegerField(null=True, blank=True) 

    def save(self, *args, **kwargs):
        """update labour subtotal on save"""
        if all([self.description, self.hours]):
            self.total = self.hours * settings.LABOUR_RATE
        else:
            self.total = None
        super().save(*args, **kwargs)

    

    
   