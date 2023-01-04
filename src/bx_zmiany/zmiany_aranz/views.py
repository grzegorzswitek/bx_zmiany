from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.views import View
from django.views.generic import (
    DetailView,
    ListView,
    CreateView,
    DeleteView,
    UpdateView,
)
from django.urls import reverse

from .models import Procedure, Cost, Invoice


class ProcedureDetailView(DetailView):

    model = Procedure
    template_name = "zmiany_aranz/procedure.html"


class ProcedureCostsList(ListView):
    model = Cost
    template_name = "zmiany_aranz/procedure_costs_list.html"

    def get_queryset(self):
        queryset = super(ProcedureCostsList, self).get_queryset()
        pk = self.kwargs["pk"]
        queryset = queryset.filter(procedures__in=[pk])
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ProcedureCostsList, self).get_context_data(**kwargs)
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


class CostCreateView(CreateView):
    model = Cost
    fields = "__all__"
    template_name = "zmiany_aranz/procedure_cost_create.html"

    def get_success_url(self) -> str:
        pk = self.kwargs.get("pk", None)
        if pk is None:
            return super().get_success_url()
        return reverse("zmiany_aranz:procedure_costs_list", kwargs={"pk": pk})

    def form_valid(self, form):
        response = super(CostCreateView, self).form_valid(form)
        pk = self.kwargs.get("pk", None)
        if pk is None:
            raise Http404
        try:
            procedure = Procedure.objects.get(pk=pk)
        except Procedure.DoesNotExist:
            return Http404
        procedure.costs.add(self.object)
        return response


class CostDeleteView(DeleteView):
    model = Cost
    template_name = "zmiany_aranz/cost_delete_confirm.html"

    def get_success_url(self) -> str:
        procedure = self.object.procedures.first()
        if procedure is None:
            return "/"
        return reverse("zmiany_aranz:procedure_costs_list", kwargs={"pk": procedure.pk})


class CostUpdateView(UpdateView):
    model = Cost
    fields = "__all__"
    template_name = "zmiany_aranz/cost_update.html"

    def get_success_url(self) -> str:
        procedure = self.object.procedures.first()
        return reverse("zmiany_aranz:procedure_costs_list", kwargs={"pk": procedure.pk})


class ProcedureInvoicesList(ListView):
    model = Invoice
    template_name = "zmiany_aranz/procedure_invoices_list.html"

    def get_queryset(self):
        queryset = super(ProcedureInvoicesList, self).get_queryset()
        pk = self.kwargs["pk"]
        queryset = queryset.filter(procedures__in=[pk])
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ProcedureInvoicesList, self).get_context_data(**kwargs)
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


class InvoiceCreateView(CreateView):
    model = Invoice
    fields = "__all__"
    template_name = "zmiany_aranz/procedure_invoice_create.html"

    def get_success_url(self) -> str:
        pk = self.kwargs.get("pk", None)
        if pk is None:
            return super().get_success_url()
        return reverse("zmiany_aranz:procedure_invoices_list", kwargs={"pk": pk})

    def form_valid(self, form):
        response = super(InvoiceCreateView, self).form_valid(form)
        pk = self.kwargs.get("pk", None)
        if pk is None:
            raise Http404
        try:
            procedure = Procedure.objects.get(pk=pk)
        except Procedure.DoesNotExist:
            return Http404
        procedure.invoices.add(self.object)
        return response


class InvoiceDeleteView(DeleteView):
    model = Invoice
    template_name = "zmiany_aranz/invoice_delete_confirm.html"

    def get_success_url(self) -> str:
        procedure = self.object.procedures.first()
        if procedure is None:
            return "/"
        return reverse(
            "zmiany_aranz:procedure_invoices_list", kwargs={"pk": procedure.pk}
        )


class InvoiceUpdateView(UpdateView):
    model = Invoice
    fields = "__all__"
    template_name = "zmiany_aranz/invoice_update.html"

    def get_success_url(self) -> str:
        procedure = self.object.procedures.first()
        return reverse(
            "zmiany_aranz:procedure_invoices_list", kwargs={"pk": procedure.pk}
        )
