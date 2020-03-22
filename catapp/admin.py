from django.contrib import admin
from catapp.models import Cat
from django.contrib.admin import ModelAdmin


class CatModel (admin.ModelAdmin):
    readonly_fields = ('id',)


admin.site.register(Cat, CatModel)