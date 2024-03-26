from django.db import models
from django.db.models import Sum
from django.conf import settings
from django.utils.text import slugify
from customer.models import Customer, Vehicle
from django.utils import timezone


class Invoice(models.Model):

    class InvoiceStatus(models.IntegerChoices):
        OPEN = '1', 'Open'
        READY_FOR_PROCESSING = '2', 'Ready for processing'
        READY_FOR_VERIFICATION = '3', 'Ready for verification'
        SENT_TO_CUSTOMER = '4', 'Sent to customer'
        WORK_ON_HOLD = '5', 'Work on hold'
        COMPLETE = '6', 'Complete'

    inv_number = models.CharField(
        max_length=10, null=True, editable=False)
    inv_integer = models.PositiveIntegerField(null=True, editable=False)
    customer = models.ForeignKey(
        Customer, on_delete=models.PROTECT, related_name='invoices')
    vehicle = models.ForeignKey(
        Vehicle, on_delete=models.PROTECT, related_name='invoices')
    date_in = models.DateTimeField(blank=True, null=True)
    mileage = models.PositiveIntegerField(blank=True, null=True)
    status = models.PositiveSmallIntegerField(
        choices=InvoiceStatus.choices, blank=True, null=True)
    active = models.BooleanField(default=True, blank=True, null=True)
    subtotal = models.PositiveIntegerField(blank=True, null=True)
    vat_subtotal = models.PositiveIntegerField(blank=True, null=True)
    grand_total = models.PositiveIntegerField(blank=True, null=True)

    # utilities
    slug = models.SlugField(max_length=100, unique=True, blank=False, null=False)    

    def __str__(self):
        cust = self.customer.friendly_name
        veh = self.vehicle.registration
        inv_int = self.inv_integer
        inv_num = self.inv_number
        if inv_int is not None:
            str = f'{inv_num} - {cust} - {veh}'
        elif cust and veh:
            str = f'{cust} - {veh}'
        else: 
            str = f'Blank invoice {self.pk}'
        return str

    def update_total(self):
        #update grand_total each time a part or labour entry is updated.
        part_subtotal = self.parts.aggregate(Sum('subtotal'))['subtotal__sum'] or 0
        labour_subtotal = self.labour.aggregate(Sum('subtotal'))['subtotal__sum'] or 0
        self.subtotal = part_subtotal + labour_subtotal
        if self.subtotal > 0:
            self.vat_subtotal = self.subtotal * settings.VAT_PERCENTAGE
            self.grand_total = self.subtotal + self.vat_subtotal
        else:
            self.grand_total = 0
            self.vat_subtotal = 0
        self.save()

        

    def save(self, *args, **kwargs):
        # create a todays date if no date provided
        if self.date_in is None:
            self.date_in = timezone.localtime(timezone.now())

        # Set active to True or False and create invoice number depending on invoice status.
        if self.status:
            if self.status >= 5:
                self.active = False
                if self.status == 6 and self.inv_number is not None:
                    try:
                        latest = Invoice.objects.latest('inv_integer')
                    except ObjectDoesNotExist:
                        self.inv_integer = 1
                    else:
                        self.inv_integer = latest + 1
                    self.inv_number = f'INV_#{self.inv_integer}'
            else:
                self.active = True  
            
        self.slug = slugify(f'{self}')
        super().save(*args, **kwargs)


class Part(models.Model):

    invoice = models.ForeignKey(
        Invoice, on_delete=models.PROTECT, related_name='parts')
    cost_to_company = models.PositiveIntegerField(null=True, blank=True)
    price_to_customer = models.PositiveIntegerField(null=True, blank=True)
    title = models.CharField(max_length=25, null=False, blank=False)
    quantity = models.PositiveIntegerField(default=1)
    subtotal = models.PositiveIntegerField(null=True, blank=True)

    def save(self, *args, **kwargs):
        """update part subtotal on save"""
        if self.price_to_customer: 
            self.subtotal = self.price_to_customer * self.quantity
        super().save(*args, **kwargs)


class Labour(models.Model):

    class Meta:
        verbose_name_plural = 'Labour'

    invoice = models.ForeignKey(
        Invoice, on_delete=models.PROTECT, related_name='labour')
    title = models.CharField(max_length=27, null=False, blank=False)
    description = models.CharField(max_length=250, null=True, blank=True)
    hours = models.PositiveIntegerField(default=1)
    subtotal = models.PositiveIntegerField(null=True, blank=True) 

    def save(self, *args, **kwargs):
        """update labour subtotal on save"""
        self.subtotal = self.hours * settings.LABOUR_RATE
        super().save(*args, **kwargs)

    

    
   