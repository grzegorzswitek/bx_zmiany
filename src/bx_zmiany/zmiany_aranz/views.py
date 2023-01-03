from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.views import View
from django.views.generic import DetailView, ListView

from .models import Procedure, Cost


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
