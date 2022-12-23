from django.contrib import admin

from zmiany_aranz.models import (
    Building, 
    Cost, 
    CostEstimate, 
    CostEstimateOfProcedure, 
    CustomUser, 
    Customer, 
    CustomerHandler, 
    CustomerOfProcedure, 
    Investment, 
    InvestmentStage, 
    Invoice, 
    KindOfCost, 
    KindOfPremises, 
    Person, 
    Premises, 
    Procedure,
)


class BuildingAdmin(admin.ModelAdmin):
	pass
 
class CostAdmin(admin.ModelAdmin):
	pass
 
class CostEstimateAdmin(admin.ModelAdmin):
	pass
 
class CostEstimateOfProcedureAdmin(admin.ModelAdmin):
	pass
 
class CustomUserAdmin(admin.ModelAdmin):
	pass
 
class CustomerAdmin(admin.ModelAdmin):
	pass
 
class CustomerHandlerAdmin(admin.ModelAdmin):
	pass
 
class CustomerOfProcedureAdmin(admin.ModelAdmin):
	pass
 
class InvestmentAdmin(admin.ModelAdmin):
	pass
 
class InvestmentStageAdmin(admin.ModelAdmin):
	pass
 
class InvoiceAdmin(admin.ModelAdmin):
	pass
 
class KindOfCostAdmin(admin.ModelAdmin):
	pass
 
class KindOfPremisesAdmin(admin.ModelAdmin):
	pass
 
class PersonAdmin(admin.ModelAdmin):
	pass
 
class PremisesAdmin(admin.ModelAdmin):
	pass
 
class ProcedureAdmin(admin.ModelAdmin):
	pass

admin.site.register(Building, BuildingAdmin) 
admin.site.register(Cost, CostAdmin) 
admin.site.register(CostEstimate, CostEstimateAdmin) 
admin.site.register(CostEstimateOfProcedure, CostEstimateOfProcedureAdmin) 
admin.site.register(CustomUser, CustomUserAdmin) 
admin.site.register(Customer, CustomerAdmin) 
admin.site.register(CustomerHandler, CustomerHandlerAdmin) 
admin.site.register(CustomerOfProcedure, CustomerOfProcedureAdmin) 
admin.site.register(Investment, InvestmentAdmin) 
admin.site.register(InvestmentStage, InvestmentStageAdmin) 
admin.site.register(Invoice, InvoiceAdmin) 
admin.site.register(KindOfCost, KindOfCostAdmin) 
admin.site.register(KindOfPremises, KindOfPremisesAdmin) 
admin.site.register(Person, PersonAdmin) 
admin.site.register(Premises, PremisesAdmin) 
admin.site.register(Procedure,ProcedureAdmin)
