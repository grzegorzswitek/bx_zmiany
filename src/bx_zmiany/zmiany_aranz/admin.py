from django.contrib import admin

from zmiany_aranz.models import Procedure


class ProcedureAdmin(admin.ModelAdmin):
    pass

admin.site.register(Procedure, ProcedureAdmin)