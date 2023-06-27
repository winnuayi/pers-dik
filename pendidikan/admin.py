from django.contrib import admin

from . import models


class SumberPaAdmin(admin.ModelAdmin):
    list_display = ('nama',)
    ordering = ('nama',)


admin.site.register(models.SumberPA, SumberPaAdmin)
