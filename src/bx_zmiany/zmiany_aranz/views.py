from typing import *
import logging

from django.core.exceptions import FieldError
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
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
    RedirectView,
)

from outlook.outlook import Message

from .models import (
    Procedure,
    Premises,
    CustomerOfProcedure,
    EmailAction,
    InvestmentStage,
)
from .forms import SendEmailForm, PremisesImportForm, ProcedureSearchForm
from zmiany_aranz.string_replacer import Replacer

from zmiany_aranz.apps import ZmianyAranzConfig

APP_NAME = ZmianyAranzConfig.name

logger = logging.getLogger(__name__)


class IndexView(TemplateView):
    template_name = "index.html"


class ProcedureSubpagesAbstractView(View):
    extra_context = {"ctx_menu_template": "zmiany_aranz/procedure-ctx-menu.html"}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get("pk")
        try:
            procedure = Procedure.objects.get(pk=pk)
        except Procedure.DoesNotExist:
            raise Http404
        investment_stage = procedure.investment_stage
        email_actions = None
        if investment_stage:
            email_actions = EmailAction.objects.filter(
                investment_stage=investment_stage.pk
            )
        context.update({"procedure": procedure, "email_actions": email_actions})
        return context


class ProcedureDetailView(ProcedureSubpagesAbstractView, DetailView):

    model = Procedure
    template_name = f"{APP_NAME}/procedure.html"
    context_object_name = "procedure"
    extra_context = {"ctx_menu_template": "zmiany_aranz/procedure-ctx-menu.html"}

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context_data = super().get_context_data(**kwargs)
        investment_stage = self.object.investment_stage
        if isinstance(investment_stage, InvestmentStage):
            email_actions = EmailAction.objects.filter(
                investment_stage=investment_stage.pk
            )
            context_data.update({"email_actions": email_actions})
        return context_data


class ProcedureCreateRedirect(RedirectView):
    """Create a procedure for a given premises and redirect to the
    details of the procedure."""

    def get_redirect_url(self, *args: Any, **kwargs: Any) -> Optional[str]:
        premises_pk = self.request.GET.get("premises", None)
        if premises_pk is None:
            messages.error(self.request, "The GET 'premises' parameter is not set.")
            return self.request.headers.get("referer", "/")
        try:
            premises = Premises.objects.get(pk=premises_pk)
        except Premises.DoesNotExist:
            messages.error(self.request, "Premises does not exist.")
            return self.request.headers.get("referer", "/")
        procedure = Procedure.objects.create()
        procedure.premises.set([premises])
        procedure.save()
        messages.success(self.request, "The procedure has been created.")
        return procedure.get_absolute_url()


class ProcedureListView(ListView):
    model = Procedure
    paginate_by = 30
    template_name = f"{APP_NAME}/procedure_list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = object_list if object_list is not None else self.object_list

        form = ProcedureSearchForm(self.request.GET)
        if form.is_valid():
            investments = form.cleaned_data.get("investment")
            investment_stages = form.cleaned_data.get("investment_stage")
            buildings = form.cleaned_data.get("building")
            if investments:
                queryset = queryset.investment__in(investments)
            if investment_stages:
                queryset = queryset.investment_stage__in(investment_stages)
            if buildings:
                queryset = queryset.building__in(buildings)

        return super().get_context_data(form=form, object_list=queryset, **kwargs)


class ProcedureUpdateView(ProcedureSubpagesAbstractView, UpdateView):
    model = Procedure
    template_name = f"{APP_NAME}/procedure_update.html"
    fields = [
        "premises",
        "customer_handler",
        "status",
        "invoice_status",
        "invoice_month",
        "gross_fee_for_arran_changes",
        "accepted",
        "directory",
        "comment",
    ]


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


class ProcedureCustomersList(ProcedureSubpagesListView):
    model = CustomerOfProcedure
    template_name = f"{APP_NAME}/procedure_customers_list.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        pk = self.kwargs["pk"]
        queryset = queryset.filter(procedure__in=[pk])
        return queryset

    def get(self, request, *args, **kwargs):
        pk = self.kwargs["pk"]
        try:
            Procedure.objects.get(pk=pk)
        except Procedure.DoesNotExist:
            raise Http404
        return super().get(request, *args, **kwargs)


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


class SendEmailView(FormView):
    template_name = f"{APP_NAME}/send_email.html"
    form_class = SendEmailForm
    success_url = "."

    def get_initial(self):
        initial = super().get_initial()
        recipients = self.action.get_recipients()
        procedure_replacer = Replacer(self.procedure)
        attachment_seq = self.action.get_attachments_to_form(self.procedure)
        mail_subject, mail_body = [
            procedure_replacer(getattr(self.action, field))
            if getattr(self.action, field) is not None
            else ""
            for field in ["mail_subject", "mail_body"]
        ]
        initial.update(
            {
                "to": "\r\n".join(recipients["TO"]),
                "cc": "\r\n".join(recipients["CC"]),
                "bcc": "\r\n".join(recipients["BCC"]),
                "subject": mail_subject,
                "body": mail_body,
                "attachments": [id for (id, _) in attachment_seq],
            }
        )
        return initial

    def get_form_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_form_kwargs()
        kwargs.update(
            {"attachments_choices": self.action.get_attachments_to_form(self.procedure)}
        )
        return kwargs

    def form_valid(self, form) -> HttpResponse:
        attachemnts_ids = form.cleaned_data["attachments"]
        attachemnts_paths = self.action.get_attachments_by_id(
            self.procedure, attachemnts_ids
        )
        message_data = form.cleaned_data
        message_data["attachments"] = attachemnts_paths
        try:
            message = Message(**message_data)
            message.create()
            message.save()
        except Exception as e:
            messages.error(
                self.request, f"Nie udało się utworzyć wiadomości e-mail. {e}."
            )
            return super().get(
                self.request,
                context={"error": f"Nie udało się utworzyć wiadomości e-mail ({e})."},
            )
        messages.success(self.request, "Wiadomość została utworzona (wersje robocze).")
        return super().form_valid(form)

    def dispatch(self, request, *args: Any, **kwargs: Any) -> HttpResponse:
        action_name = kwargs.get("slug", None)
        procedure_pk = kwargs.get("pk", None)
        try:
            self.procedure = Procedure.objects.get(pk=procedure_pk)
        except Procedure.DoesNotExist:
            raise Http404("Procedure DoesNotExist")
        self.investment_stage = self.procedure.investment_stage
        if self.investment_stage is None:
            raise Http404("InvestmentStage is None")
        try:
            self.action = EmailAction.objects.get(
                investment_stage=self.investment_stage, slug=action_name
            )
        except EmailAction.DoesNotExist:
            raise Http404("EmailAction DoesNotExist")
        return super().dispatch(request, *args, **kwargs)


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
