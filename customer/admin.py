from django.contrib import admin
from .models import Customer, Vehicle

class CustomerAdmin(admin.ModelAdmin):

    readonly_fields = ('slug',)

class VehicleAdmin(admin.ModelAdmin):

    readonly_fields = ('slug',)


# Register your models here.
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Vehicle, VehicleAdmin)