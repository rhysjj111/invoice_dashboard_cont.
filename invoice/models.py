from django.db import models
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

    invoice_number = models.CharField(
        max_length=10, null=True, editable=False)
    invoice_int = models.PositiveIntegerField(null=True, editable=False)
    customer = models.ForeignKey(
        Customer, on_delete=models.PROTECT, related_name='invoices')
    vehicle = models.ForeignKey(
        Vehicle, on_delete=models.PROTECT, related_name='invoices')
    date_in = models.DateTimeField(blank=True, null=True)
    mileage = models.PositiveIntegerField(blank=True, null=True)
    status = models.PositiveSmallIntegerField(
        choices=InvoiceStatus.choices, blank=True, null=True)
    active = models.BooleanField(default=True, blank=True, null=True)
    sub_total = models.PositiveIntegerField(blank=True, null=True)
    grand_total = models.PositiveIntegerField(blank=True, null=True)

    # utilities
    slug = models.SlugField(max_length=100, unique=True, blank=False, null=False)    

    def __str__(self):
        cust = self.customer.friendly_name
        veh = self.vehicle.registration
        inv_int = self.invoice_int
        inv_num = self.invoice_number
        if inv_int is not None:
            str = f'{inv_num} - {cust} - {veh}'
        elif cust and veh:
            str = f'{cust} - {veh}'
        else: 
            str = 'Blank invoice'
        return str

    def save(self, *args, **kwargs):
        # create a todays date if no date provided
        if self.date_in is None:
            self.date_in = timezone.localtime(timezone.now())
        
        # DONT FORGET TO ADD CHANGE OF ACTIVE WHEN INVOICE CHANGED TO WORK ON HOLD OR COMPLETE

        # Set active to True or False and create invoice number depending on invoice status.
        if self.status == 6:
            if self.invoice_number is not None:
                try:
                    latest = Invoice.objects.latest('invoice_int')
                except ObjectDoesNotExist:
                    self.invoice_int = 1
                else:
                    self.invoice_int = latest + 1
                self.invoice_number = f'INV_#{self.invoice_int}'
            self.active = False
        elif self.status == 5:
            self.active = False
        else:
            self.active = True
                 
            
        self.slug = slugify(f'{self.name}')
        super().save(*args, **kwargs)

    
   