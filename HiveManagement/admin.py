from django.contrib.gis import admin
from .models import Field, Tag, PalletReport

class FieldAdmin(admin.GeoModelAdmin):
    list_display = ('name', 'locality', 'county', 'state', 'date_added', 'owner', 'source_region')

class TagAdmin(admin.ModelAdmin):
    list_display= ('id', 'uniqueTID')

class TagCheckInInline(admin.TabularInline):
    model = PalletReport

# Register your models here.
admin.site.register(Field, FieldAdmin)
admin.site.register(Tag,TagAdmin)

