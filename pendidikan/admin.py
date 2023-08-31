from django.contrib import admin

from . import models


class SumberPaAdmin(admin.ModelAdmin):
    list_display = ('nama',)
    ordering = ('nama',)


class PangkatAdmin(admin.ModelAdmin):
    list_display = ('nama', 'counter',)
    ordering = ('counter',)

admin.site.register(models.Pangkat, PangkatAdmin)
admin.site.register(models.SumberPa, SumberPaAdmin)
