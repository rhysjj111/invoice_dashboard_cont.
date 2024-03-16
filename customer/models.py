from django.db import models
from django.utils.text import slugify 


class Customer(models.Model):
    

    class CustomerType(models.IntegerChoices):
        TRADE = '1', 'Trade'
        PRIVATE = '2', 'Private'


    class PaymentTerms(models.IntegerChoices):
        PIA = '1', 'Payment in advance'
        NET_7 = '2', '7 days'
        NET_14 = '3', '14 days'
        NET_30 = '4', '30 days'
        NET_60 = '5', '60 days'


    name = models.CharField(max_length=20, blank=False, null=False)
    friendly_name = models.CharField(max_length=10, blank=True, null=True)
    type = models.PositiveSmallIntegerField(
        choices=CustomerType.choices, blank=True, null=True)
    address_line_1 = models.CharField(max_length=27, blank=True, null=True)
    address_line_2 = models.CharField(max_length=27, blank=True, null=True)
    city_region = models.CharField(max_length=27, blank=True, null=True)
    post_code = models.CharField(max_length=10, blank=True, null=True)
    contact_number_primary = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=20, blank=True, null=True)
    payment_terms = models.PositiveSmallIntegerField(
        choices=PaymentTerms.choices, blank=True, null=True)
    active = models.BooleanField(default=True, blank=True, null=True)

    # utilities
    slug = models.SlugField(max_length=100, unique=True, blank=False, null=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(f'{self.name}')
        super().save(*args, **kwargs)


class Vehicle(models.Model):

    customer_id = models.ForeignKey(
        Customer, blank=False, null=False, on_delete=models.CASCADE)
    registration = models.CharField(max_length=10, null=False, blank=False)
    make = models.CharField(max_length=27, blank=True, null=True)
    model = models.CharField(max_length=27, blank=True, null=True)
    active = models.BooleanField(default=True, blank=True, null=True)

    # utilities
    slug = models.SlugField(max_length=100, unique=True, blank=False, null=False)

    def __str__(self):
        return self.registration

    def save(self, *args, **kwargs):
        self.slug = slugify(f'{self.registration}')
        super().save(*args, **kwargs)

    
    


    
    

