from django.contrib import admin
from .models import CarMake, CarModel


class CarModelInline(admin.StackedInline):
    model = CarModel


class CarModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'year', 'make', 'name', 'model_type', 'dealerId')
    list_display_links = ('id', 'name')


class CarMakeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'country')
    list_display_links = ('id', 'name')
    inlines = [CarModelInline]


admin.site.register(CarModel, CarModelAdmin)
admin.site.register(CarMake, CarMakeAdmin)
