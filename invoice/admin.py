from django.contrib import admin
from .models import Invoice, Part, Labour
from django.utils.dateformat import format

class PartAdminInline(admin.TabularInline):
    model = Part
    readonly_fields = ('total',)

class LabourAdminInline(admin.TabularInline):
    model = Labour
    readonly_fields = ('total',)

class InvoiceAdmin(admin.ModelAdmin):
    inlines = (PartAdminInline, LabourAdminInline)

    readonly_fields = ('inv_number', 'inv_integer', 'parts_total',
                       'labour_total', 'subtotal', 'vat_total',
                       'grand_total', 'slug', 'unique_id',)
    
    list_display = ('__str__', 'formatted_date_in', 'grand_total',)

    def formatted_date_in(self, obj):
        return format(obj.date_in, 'd/m/Y')

    formatted_date_in.short_description = 'Date In'
    ordering = ('-date_in',)
    
# Register your models here.
admin.site.register(Invoice, InvoiceAdmin)