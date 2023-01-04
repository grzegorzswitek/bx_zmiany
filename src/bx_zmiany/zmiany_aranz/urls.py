from django.urls import path
from zmiany_aranz.views import (
    ProcedureDetailView,
    ProcedureCostsList,
    CostCreateView,
    CostDeleteView,
)

app_name = "zmiany_aranz"

urlpatterns = [
    path(
        "procedure/<int:pk>/",
        ProcedureDetailView.as_view(),
        name="procedure_detail_view",
    ),
    path(
        "procedure/<int:pk>/cost/list/",
        ProcedureCostsList.as_view(),
        name="procedure_costs_list",
    ),
    path(
        "procedure/<int:pk>/cost/add/",
        CostCreateView.as_view(),
        name="procedure_cost_create",
    ),
    path(
        "cost/<int:pk>/delete/",
        CostDeleteView.as_view(),
        name="cost_delete",
    ),
]
