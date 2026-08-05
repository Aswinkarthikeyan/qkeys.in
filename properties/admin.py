from django.contrib import admin
from .models import Location, BHKType, Amenity, Property

from django.contrib import admin
from .models import *

admin.site.register(Location)
admin.site.register(BHKType)
admin.site.register(Amenity)
admin.site.register(Property)

@admin.register(ContactInquiry)
class ContactAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "phone",
        "visit_date",
        "visit_time",
        "purpose"
    )