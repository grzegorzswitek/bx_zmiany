from django.urls import path
from zmiany_aranz.views import (
    ProcedureDetailView,
    ProcedureCostsList,
    CostCreateView,
    CostUpdateView,
    CostDeleteView,
    ProcedureInvoicesList,
    InvoiceCreateView,
    InvoiceUpdateView,
    InvoiceDeleteView,
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
        "cost/<int:pk>/update/",
        CostUpdateView.as_view(),
        name="cost_update",
    ),
    path(
        "cost/<int:pk>/delete/",
        CostDeleteView.as_view(),
        name="cost_delete",
    ),
    path(
        "procedure/<int:pk>/invoice/list/",
        ProcedureInvoicesList.as_view(),
        name="procedure_invoices_list",
    ),
    path(
        "procedure/<int:pk>/invoice/add/",
        InvoiceCreateView.as_view(),
        name="procedure_invoice_create",
    ),
    path(
        "invoice/<int:pk>/update/",
        InvoiceUpdateView.as_view(),
        name="invoice_update",
    ),
    path(
        "invoice/<int:pk>/delete/",
        InvoiceDeleteView.as_view(),
        name="invoice_delete",
    ),
]
