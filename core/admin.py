# locations/admin.py
from django.contrib import admin

from .base_admin import BaseTabularInline, BaseModelAdmin
from .models import Country, Region, City


class RegionInline(BaseTabularInline):
    model = Region
    extra = 1
    fields = ('name', 'code')
class CityInline(BaseTabularInline):
    model = City
    extra = 1

@admin.register(Country)
class CountryAdmin(BaseModelAdmin):

    list_display = ('name', 'code')
    search_fields = ('name',)
    inlines = [RegionInline] # دمج المناطق داخل الدولة

@admin.register(Region)
class RegionAdmin(BaseModelAdmin):
    list_display = ('name', 'code', 'country')
    list_filter = ('country',) # يمكنك الفلترة حسب الدولة
    search_fields = ('name',)
    inlines = [CityInline] # إضافة المدن هنا لسهولة الإدخال

@admin.register(City)
class CityAdmin(BaseModelAdmin):
    list_display = ('name', 'region')
    list_filter = ('region__country', 'region') # فلترة هرمية (دولة ثم منطقة)
    search_fields = ('name',)