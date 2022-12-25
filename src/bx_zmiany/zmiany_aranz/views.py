from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.views.generic import DetailView

from .models import (
    Procedure,
)


class ProcedureDetailView(DetailView):

    model = Procedure
    template_name = "zmiany_aranz/procedure.html"
