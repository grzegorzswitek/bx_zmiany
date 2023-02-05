from typing import *
import logging

from django.core.exceptions import FieldError
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.views import View
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    DetailView,
    ListView,
    CreateView,
    DeleteView,
    UpdateView,
    TemplateView,
    FormView,
)

from outlook.outlook import Message

from .models import (
    Procedure,
    Premises,
    Customer,
    CustomerOfProcedure,
    EmailAction,
    InvestmentStage,
)
from .forms import SendEmailForm, PremisesImportForm
from zmiany_aranz.string_replacer import Replacer

from zmiany_aranz.apps import ZmianyAranzConfig

APP_NAME = ZmianyAranzConfig.name

logger = logging.getLogger(__name__)


class IndexView(TemplateView):
    template_name = "index.html"


class ProcedureSubpagesAbstractView(View):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get("pk")
        try:
            context["procedure"] = Procedure.objects.get(pk=pk)
        except Procedure.DoesNotExist:
            raise Http404
        return context


class ProcedureDetailView(ProcedureSubpagesAbstractView, DetailView):

    model = Procedure
    template_name = f"{APP_NAME}/procedure.html"
    context_object_name = "procedure"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context_data = super().get_context_data(**kwargs)
        investment_stage = self.object.investment_stage
        if isinstance(investment_stage, InvestmentStage):
            email_actions = EmailAction.objects.filter(
                investment_stage=investment_stage.pk
            )
            context_data.update({"email_actions": email_actions})
        return context_data


class ProcedureSubpagesListView(ProcedureSubpagesAbstractView, ListView):
    def get_queryset(self):
        queryset = super().get_queryset()
        pk = self.kwargs.get("pk")
        try:
            queryset = queryset.filter(procedures__in=[pk])
        except FieldError:
            queryset = queryset.filter(procedure__in=[pk])
        return queryset


class ProcedureSubpagesCreateView(ProcedureSubpagesAbstractView, CreateView):
    success_url_name = ""
    related_field_name = ""

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
            related_field = getattr(self.procedure, self.related_field_name)
            related_field.add(self.object)
            return response
        except Procedure.DoesNotExist:
            return Http404
        except AttributeError as e:
            raise ValueError("related_field_name is not valid.") from e


class ProcedureSubpagesDeleteView(DeleteView):
    success_url_name = ""

    def get_success_url(self) -> str:
        try:
            procedure = self.object.procedures.first()
        except AttributeError:
            procedure = self.object.procedure
        if procedure is None:
            return "/"
        return reverse(
            f"{APP_NAME}:{self.success_url_name}", kwargs={"pk": procedure.pk}
        )


class ProcedureSubpagesUpdateView(UpdateView):
    success_url_name = ""

    def get_success_url(self) -> str:
        procedure = self.object.procedures.first()
        return reverse(
            f"{APP_NAME}:{self.success_url_name}", kwargs={"pk": procedure.pk}
        )


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


class CustomerOfProcedureAbstractView(View):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        procedure = self.object.procedure
        if procedure:
            context["procedure"] = procedure
        else:
            raise Http404
        return context

    def get_success_url(self) -> str:
        procedure = self.object.procedure
        if procedure is None:
            return "/"
        return reverse(
            f"{APP_NAME}:procedure_customers_list", kwargs={"pk": procedure.pk}
        )


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


class CustomerOfProcedureDeleteView(CustomerOfProcedureAbstractView, DeleteView):
    model = CustomerOfProcedure
    template_name = f"{APP_NAME}/customer_of_procedure_delete_confirm.html"


class CustomerOfProcedureUpdateView(CustomerOfProcedureAbstractView, UpdateView):
    model = CustomerOfProcedure
    fields = "__all__"
    template_name = f"{APP_NAME}/customer_of_procedure_update.html"

    def get_form(self):
        form = super().get_form()
        form.fields["procedure"].disabled = True
        return form


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
        mail_subject, mail_body = [
            procedure_replacer(getattr(action, field))
            if getattr(action, field) is not None
            else ""
            for field in ["mail_subject", "mail_body"]
        ]
        initial = {
            "to": "\r\n".join(recipients["to"]),
            "cc": "\r\n".join(recipients["cc"]),
            "bcc": "\r\n".join(recipients["bcc"]),
            "subject": mail_subject,
            "body": mail_body,
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


class PremisesImportView(SuccessMessageMixin, FormView):
    """View for importing multiple premises from a data file."""

    template_name = f"{APP_NAME}/premises_import.html"
    form_class = PremisesImportForm
    success_url = "."

    def form_valid(self, form) -> HttpResponse:
        if form.added_premises:
            messages.success(
                self.request,
                f"{form.added_premises} premises have been added to the database.",
            )
        return super().form_valid(form)


class PremisesSymbolRedirectView(View):
    """Redirect to the procedure if the premises
    is assigned to it or to the premises otherwise.
    Redirect to the home page if the premises does not exist."""

    home_url = reverse_lazy(f"{APP_NAME}:index")

    def get(self, request, *args, **kwargs):
        symbol = request.GET.get("premises-symbol")
        if not symbol:
            messages.warning(request, "Bad form")
            return HttpResponseRedirect(self.home_url)
        try:
            premises = Premises.objects.get(symbol__iexact=symbol)
        except Premises.DoesNotExist:
            messages.warning(request, "Premises not found.")
            return HttpResponseRedirect(self.home_url)
        procedure = Procedure.objects.filter(premises=premises).last()
        if not procedure:
            return HttpResponseRedirect(
                reverse(f"{APP_NAME}:premises_detail", kwargs={"pk": premises.pk})
            )
        return HttpResponseRedirect(
            reverse(f"{APP_NAME}:procedure_detail_view", kwargs={"pk": procedure.pk})
        )
