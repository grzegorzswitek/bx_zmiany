from typing import *

from typing import *

from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.views import View
from django.views.generic import (
    DetailView,
    ListView,
    CreateView,
    DeleteView,
    UpdateView,
    TemplateView,
)
from django.urls import reverse

from .models import Procedure, Cost, Invoice, Customer, CustomerOfProcedure

from zmiany_aranz.apps import ZmianyAranzConfig

APP_NAME = ZmianyAranzConfig.name


class IndexView(TemplateView):
    template_name = "index.html"


class ProcedureDetailView(DetailView):

    model = Procedure
    template_name = f"{APP_NAME}/procedure.html"


class ProcedureSubpagesAbstractListView(ListView):
    def get_queryset(self):
        queryset = super().get_queryset()
        pk = self.kwargs["pk"]
        queryset = queryset.filter(procedures__in=[pk])
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs["pk"]
        try:
            context["procedure"] = Procedure.objects.get(pk=pk)
        except Procedure.DoesNotExist:
            context["procedure"] = None
        return context

    def get(self, request, *args, **kwargs):
        pk = self.kwargs["pk"]
        try:
            Procedure.objects.get(pk=pk)
        except Procedure.DoesNotExist:
            raise Http404
        return super().get(request, *args, **kwargs)


class ProcedureSubpagesAbstractCreateView(CreateView):
    url_name = ""

    def get_success_url(self) -> str:
        pk = self.kwargs.get("pk", None)
        if pk is None:
            return super().get_success_url()
        return reverse(f"{APP_NAME}:{self.url_name}", kwargs={"pk": pk})

    def form_valid(self, form):
        response = super().form_valid(form)
        pk = self.kwargs.get("pk", None)
        if pk is None:
            raise Http404
        try:
            self.procedure = Procedure.objects.get(pk=pk)
            return response
        except Procedure.DoesNotExist:
            return Http404


class ProcedureSubpagesAbstractDeleteView(DeleteView):
    url_name = ""

    def get_success_url(self) -> str:
        procedure = self.object.procedures.first()
        if procedure is None:
            return "/"
        return reverse(f"{APP_NAME}:{self.url_name}", kwargs={"pk": procedure.pk})


class ProcedureSubpagesAbstractUpdateView(UpdateView):
    ulr_name = ""

    def get_success_url(self) -> str:
        procedure = self.object.procedures.first()
        return reverse(f"{APP_NAME}:{self.url_name}", kwargs={"pk": procedure.pk})


class ProcedureCostsList(ProcedureSubpagesAbstractListView):
    model = Cost
    template_name = f"{APP_NAME}/procedure_costs_list.html"


class CostCreateView(ProcedureSubpagesAbstractCreateView):
    model = Cost
    fields = "__all__"
    template_name = f"{APP_NAME}/procedure_cost_create.html"
    url_name = "procedure_costs_list"

    def form_valid(self, form):
        response = super().form_valid(form)
        self.procedure.costs.add(self.object)
        return response


class CostDeleteView(ProcedureSubpagesAbstractDeleteView):
    model = Cost
    template_name = f"{APP_NAME}/cost_delete_confirm.html"
    url_name = "procedure_costs_list"


class CostUpdateView(ProcedureSubpagesAbstractUpdateView):
    model = Cost
    fields = "__all__"
    template_name = f"{APP_NAME}/cost_update.html"
    url_name = "procedure_costs_list"


class ProcedureInvoicesList(ProcedureSubpagesAbstractListView):
    model = Invoice
    template_name = f"{APP_NAME}/procedure_invoices_list.html"


class InvoiceCreateView(ProcedureSubpagesAbstractCreateView):
    model = Invoice
    fields = "__all__"
    template_name = f"{APP_NAME}/procedure_invoice_create.html"
    url_name = "procedure_invoices_list"

    def form_valid(self, form):
        response = super().form_valid(form)
        self.procedure.invoices.add(self.object)
        return response


class InvoiceDeleteView(ProcedureSubpagesAbstractDeleteView):
    model = Invoice
    template_name = f"{APP_NAME}/invoice_delete_confirm.html"
    url_name = "procedure_invoices_list"


class InvoiceUpdateView(ProcedureSubpagesAbstractUpdateView):
    model = Invoice
    fields = "__all__"
    template_name = f"{APP_NAME}/invoice_update.html"
    url_name = "procedure_invoices_list"


class ProcedureCustomersList(ListView):
    model = CustomerOfProcedure
    template_name = f"{APP_NAME}/procedure_customers_list.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        pk = self.kwargs["pk"]
        queryset = queryset.filter(procedure__in=[pk])
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs["pk"]
        try:
            context["procedure"] = Procedure.objects.get(pk=pk)
        except Procedure.DoesNotExist:
            context["procedure"] = None
        return context

    def get(self, request, *args, **kwargs):
        pk = self.kwargs["pk"]
        try:
            Procedure.objects.get(pk=pk)
        except Procedure.DoesNotExist:
            raise Http404
        return super().get(request, *args, **kwargs)


class CustomerOfProcedureCreateView(CreateView):
    model = CustomerOfProcedure
    fields = "__all__"
    template_name = f"{APP_NAME}/procedure_customer_create.html"

    def get_success_url(self) -> str:
        pk = self.kwargs.get("pk", None)
        if pk is None:
            return super().get_success_url()
        return reverse(f"{APP_NAME}:procedure_customers_list", kwargs={"pk": pk})


class CustomerOfProcedureDeleteView(DeleteView):
    model = CustomerOfProcedure
    template_name = f"{APP_NAME}/customer_of_procedure_delete_confirm.html"

    def get_success_url(self) -> str:
        procedure = self.object.procedure
        if procedure is None:
            return "/"
        return reverse(
            f"{APP_NAME}:procedure_customers_list", kwargs={"pk": procedure.pk}
        )


class CustomerOfProcedureUpdateView(UpdateView):
    model = CustomerOfProcedure
    fields = "__all__"
    template_name = f"{APP_NAME}/customer_of_procedure_update.html"

    def get_success_url(self) -> str:
        procedure = self.object.procedure
        return reverse(
            f"{APP_NAME}:procedure_customers_list", kwargs={"pk": procedure.pk}
        )


class CustomerCreateView(CreateView):
    """Class for Customer creating."""

    model = Customer
    fields = "__all__"


class CustomerDetailView(DetailView):
    """DetailView for Customer model."""

    model = Customer


class CustomerUpdateView(UpdateView):
    """UpdateView for Customer model."""

    model = Customer
    fields = "__all__"


class CustomerDeleteView(DeleteView):
    """DeleteView for Customer model."""

    model = Customer
    success_url = "/"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        result = super().get_context_data(**kwargs)
        if self.object is not None:
            result.update({"assigned_to_procedures": self.object.procedures.all()})
        return result


class ProcedureCustomersList(ListView):
    model = CustomerOfProcedure
    template_name = f"{APP_NAME}/procedure_customers_list.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        pk = self.kwargs["pk"]
        queryset = queryset.filter(procedure__in=[pk])
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs["pk"]
        try:
            context["procedure"] = Procedure.objects.get(pk=pk)
        except Procedure.DoesNotExist:
            context["procedure"] = None
        return context

    def get(self, request, *args, **kwargs):
        pk = self.kwargs["pk"]
        try:
            Procedure.objects.get(pk=pk)
        except Procedure.DoesNotExist:
            raise Http404
        return super().get(request, *args, **kwargs)


class CustomerOfProcedureCreateView(CreateView):
    model = CustomerOfProcedure
    fields = "__all__"
    template_name = f"{APP_NAME}/procedure_customer_create.html"

    def get_initial(self) -> Dict[str, Any]:
        initial = super().get_initial()
        pk = self.kwargs.get("pk", None)
        if pk is None:
            return initial
        try:
            procedure = Procedure.objects.get(pk=pk)
        except Procedure.DoesNotExist:
            return initial
        initial.update({"procedure": procedure})
        return initial

    def get_form(self):
        form = super().get_form()
        form.fields["procedure"].disabled = True
        return form

    def get_success_url(self) -> str:
        pk = self.kwargs.get("pk", None)
        if pk is None:
            return super().get_success_url()
        return reverse(f"{APP_NAME}:procedure_customers_list", kwargs={"pk": pk})


class CustomerOfProcedureDeleteView(DeleteView):
    model = CustomerOfProcedure
    template_name = f"{APP_NAME}/customer_of_procedure_delete_confirm.html"

    def get_success_url(self) -> str:
        procedure = self.object.procedure
        if procedure is None:
            return "/"
        return reverse(
            f"{APP_NAME}:procedure_customers_list", kwargs={"pk": procedure.pk}
        )


class CustomerOfProcedureUpdateView(UpdateView):
    model = CustomerOfProcedure
    fields = "__all__"
    template_name = f"{APP_NAME}/customer_of_procedure_update.html"

    def get_form(self):
        form = super().get_form()
        form.fields["procedure"].disabled = True
        return form

    def get_success_url(self) -> str:
        procedure = self.object.procedure
        return reverse(
            f"{APP_NAME}:procedure_customers_list", kwargs={"pk": procedure.pk}
        )


class CustomerCreateView(CreateView):
    """Class for Customer creating."""

    model = Customer
    fields = "__all__"


class CustomerDetailView(DetailView):
    """DetailView for Customer model."""

    model = Customer


class CustomerUpdateView(UpdateView):
    """UpdateView for Customer model."""

    model = Customer
    fields = "__all__"


class CustomerDeleteView(DeleteView):
    """DeleteView for Customer model."""

    model = Customer
    success_url = "/"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        result = super().get_context_data(**kwargs)
        if self.object is not None:
            result.update({"assigned_to_procedures": self.object.procedures.all()})
        return result
