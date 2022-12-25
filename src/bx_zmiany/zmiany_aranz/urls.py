from django.urls import path
from zmiany_aranz.views import ProcedureDetailView

app_name = "zmiany_aranz"

urlpatterns = [
    path(
        "procedure/<int:pk>/",
        ProcedureDetailView.as_view(),
        name="procedure_detail_view",
    ),
]
