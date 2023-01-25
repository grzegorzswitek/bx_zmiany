from typing import *
import logging
from os import path
from glob import glob

from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.views import View
from django.urls import reverse
from django.views.generic import (
    DetailView,
    ListView,
    CreateView,
    DeleteView,
    UpdateView,
    TemplateView,
)

from outlook.outlook import Message

from .models import (
    Procedure,
    Cost,
    Invoice,
    Customer,
    CustomerOfProcedure,
    CostEstimate,
    EmailAction,
    InvestmentStagePerson,
)
from .forms import SendEmailForm
from zmiany_aranz.string_replacer import Replacer

from zmiany_aranz.apps import ZmianyAranzConfig

APP_NAME = ZmianyAranzConfig.name

logger = logging.getLogger(__name__)


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
    success_url_name = ""

    def get_success_url(self) -> str:
        pk = self.kwargs.get("pk", None)
        if pk is None:
            return super().get_success_url()
        return reverse(f"{APP_NAME}:{self.success_url_name}", kwargs={"pk": pk})

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
    success_url_name = ""

    def get_success_url(self) -> str:
        procedure = self.object.procedures.first()
        if procedure is None:
            return "/"
        return reverse(
            f"{APP_NAME}:{self.success_url_name}", kwargs={"pk": procedure.pk}
        )


class ProcedureSubpagesAbstractUpdateView(UpdateView):
    ulr_name = ""

    def get_success_url(self) -> str:
        procedure = self.object.procedures.first()
        return reverse(
            f"{APP_NAME}:{self.success_url_name}", kwargs={"pk": procedure.pk}
        )


class ProcedureCostsList(ProcedureSubpagesAbstractListView):
    model = Cost
    template_name = f"{APP_NAME}/procedure_costs_list.html"


class CostCreateView(ProcedureSubpagesAbstractCreateView):
    model = Cost
    fields = "__all__"
    template_name = f"{APP_NAME}/procedure_cost_create.html"
    success_url_name = "procedure_costs_list"

    def form_valid(self, form):
        response = super().form_valid(form)
        self.procedure.costs.add(self.object)
        return response


class CostDeleteView(ProcedureSubpagesAbstractDeleteView):
    model = Cost
    template_name = f"{APP_NAME}/cost_delete_confirm.html"
    success_url_name = "procedure_costs_list"


class CostUpdateView(ProcedureSubpagesAbstractUpdateView):
    model = Cost
    fields = "__all__"
    template_name = f"{APP_NAME}/cost_update.html"
    success_url_name = "procedure_costs_list"


class ProcedureInvoicesList(ProcedureSubpagesAbstractListView):
    model = Invoice
    template_name = f"{APP_NAME}/procedure_invoices_list.html"


class InvoiceCreateView(ProcedureSubpagesAbstractCreateView):
    model = Invoice
    fields = "__all__"
    template_name = f"{APP_NAME}/procedure_invoice_create.html"
    success_url_name = "procedure_invoices_list"

    def form_valid(self, form):
        response = super().form_valid(form)
        self.procedure.invoices.add(self.object)
        return response


class InvoiceDeleteView(ProcedureSubpagesAbstractDeleteView):
    model = Invoice
    template_name = f"{APP_NAME}/invoice_delete_confirm.html"
    success_url_name = "procedure_invoices_list"


class InvoiceUpdateView(ProcedureSubpagesAbstractUpdateView):
    model = Invoice
    fields = "__all__"
    template_name = f"{APP_NAME}/invoice_update.html"
    success_url_name = "procedure_invoices_list"


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


class ProcedureCostEstimatesList(ProcedureSubpagesAbstractListView):
    model = CostEstimate
    template_name = f"{APP_NAME}/procedure_cost_estimates_list.html"


class CostEstimateCreateView(ProcedureSubpagesAbstractCreateView):
    model = CostEstimate
    fields = "__all__"
    template_name = f"{APP_NAME}/procedure_cost_estimate_create.html"
    success_url_name = "procedure_cost_estimates_list"

    def form_valid(self, form):
        response = super().form_valid(form)
        self.procedure.cost_estimates.add(self.object)
        return response


class CostEstimateDeleteView(ProcedureSubpagesAbstractDeleteView):
    model = CostEstimate
    template_name = f"{APP_NAME}/cost_estimate_delete_confirm.html"
    success_url_name = "procedure_cost_estimates_list"


class CostEstimateUpdateView(ProcedureSubpagesAbstractUpdateView):
    model = CostEstimate
    fields = "__all__"
    template_name = f"{APP_NAME}/cost_estimate_update.html"
    success_url_name = "procedure_cost_estimates_list"


class SendEmailView(View):
    template_name = f"{APP_NAME}/send_email.html"
    form_class = SendEmailForm

    def request_decorator(func):
        def wrapper_request_decorator(self, request, *args, **kwargs):
            # After request method (get or post).
            action_name = kwargs.get("slug", None)
            procedure_pk = kwargs.get("pk", None)
            try:
                procedure = Procedure.objects.get(pk=procedure_pk)
            except Procedure.DoesNotExist:
                logger.warning("Procedure DoesNotExist")
                raise Http404("Procedure DoesNotExist")
            investment_stage = procedure.investment_stage
            if investment_stage is None:
                logger.warning("InvestmentStage is None")
                raise Http404("InvestmentStage is None")
            try:
                action = EmailAction.objects.get(
                    investment_stage=investment_stage, slug=action_name
                )
            except EmailAction.DoesNotExist:
                logger.warning("EmailAction DoesNotExist")
                raise Http404("EmailAction DoesNotExist")
            # Call request method (get or post).
            result = func(self, request, procedure, action, *args, **kwargs)
            return result

        return wrapper_request_decorator

    @request_decorator
    def get(self, request, procedure, action, *args, **kwargs):
        recipients = action.get_recipients()
        procedure_replacer = Replacer(procedure)
        attachment_seq = action.get_attachments_to_form(procedure)
        initial = {
            "to": "\r\n".join(recipients["to"]),
            "cc": "\r\n".join(recipients["cc"]),
            "bcc": "\r\n".join(recipients["bcc"]),
            "subject": procedure_replacer(action.mail_subject),
            "body": procedure_replacer(action.mail_body),
            "attachments": [id for (id, _) in attachment_seq],
        }
        form = self.form_class(initial=initial, attachments_choices=attachment_seq)
        return render(request, self.template_name, context={"form": form})

    @request_decorator
    def post(self, request, procedure, action, *args, **kwargs):
        attachment_seq = action.get_attachments_to_form(procedure)
        form = self.form_class(request.POST, attachments_choices=attachment_seq)
        if not form.is_valid():
            return render(request, self.template_name, context={"form": form})
        attachemnts_ids = form.cleaned_data["attachments"]
        attachemnts_paths = action.get_attachments_by_id(procedure, attachemnts_ids)
        message_data = form.cleaned_data
        message_data["attachments"] = attachemnts_paths
        try:
            message = Message(**message_data)
            message.create()
            message.save()
        except Exception as e:
            return render(
                request,
                self.template_name,
                context={"error": f"Nie udało się utworzyć wiadomości e-mail ({e})."},
            )
        return render(
            request,
            self.template_name,
            context={"success": True},
        )
