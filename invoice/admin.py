from django.contrib import admin
from .models import Invoice, Part, Labour

# Register your models here.
admin.site.register(Invoice)
admin.site.register(Part)
admin.site.register(Labour)