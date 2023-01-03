from django.urls import path
from zmiany_aranz.views import ProcedureDetailView, ProcedureCostsList

app_name = "zmiany_aranz"

urlpatterns = [
    path(
        "procedure/<int:pk>/",
        ProcedureDetailView.as_view(),
        name="procedure_detail_view",
    ),
    path(
        "procedure/<int:pk>/costs/",
        ProcedureCostsList.as_view(),
        name="procedure_costs_list",
    ),
]
