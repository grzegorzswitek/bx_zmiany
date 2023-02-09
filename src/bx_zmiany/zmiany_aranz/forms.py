from typing import *
import csv

from django import forms
from django.core.validators import FileExtensionValidator

from .models import (
    Building,
    KindOfPremises,
    Premises,
    InvestmentStage,
    Investment,
)
from .validators import PremisesImportDataValidator

from utils.forms.fields import MultiEmailRecipientField


class SendEmailForm(forms.Form):
    """Send Email form definition."""

    to = MultiEmailRecipientField(
        delimiter="\r\n",
        required=False,
        widget=forms.Textarea(attrs={"rows": 5}),
    )
    cc = MultiEmailRecipientField(
        delimiter="\r\n",
        required=False,
        widget=forms.Textarea(attrs={"rows": 5}),
    )
    bcc = MultiEmailRecipientField(
        delimiter="\r\n",
        required=False,
        widget=forms.Textarea(attrs={"rows": 5}),
    )
    subject = forms.CharField(max_length=77)
    body = forms.CharField(widget=forms.Textarea(attrs={"rows": 10}))
    attachments = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple(),
    )

    def __init__(self, *args, **kwargs):
        attachments_choices = kwargs.pop("attachments_choices", [])
        super().__init__(*args, **kwargs)
        self.fields["attachments"].choices = attachments_choices


class PremisesImportForm(forms.Form):
    fieldnames = [
        "id_crm",
        "symbol",
        "building_symbol",
        "kind_symbol",
        "staircase",
        "storey",
    ]
    added_premises = None

    file = forms.FileField(
        validators=[
            FileExtensionValidator(["csv"]),
            PremisesImportDataValidator(fieldnames),
        ]
    )

    def _add_premises(self):
        buildings = {
            building_object.symbol: building_object
            for building_object in Building.objects.all()
        }
        kinds_of_premises = {
            kind_of_premises_object.symbol: kind_of_premises_object
            for kind_of_premises_object in KindOfPremises.objects.all()
        }
        csv_file = self.files["file"]
        csv_file.open()
        reader = csv.DictReader(
            csv_file.file.read().decode("utf-8-sig").split("\n")[1:],
            fieldnames=self.fieldnames,
            delimiter=";",
        )
        premises_list = [
            Premises(
                id_crm=row["id_crm"],
                symbol=row["symbol"],
                building=buildings.get(row["building_symbol"]),
                kind=kinds_of_premises.get(row["kind_symbol"]),
                staircase=row["staircase"],
                storey=row["storey"],
            )
            for row in reader
        ]
        Premises.objects.bulk_create(premises_list)
        self.added_premises = len(premises_list)

    def is_valid(self) -> bool:
        is_valid = super().is_valid()
        if not is_valid:
            return is_valid
        self._add_premises()
        return is_valid


class ProcedureSearchForm(forms.Form):
    investment = forms.ModelMultipleChoiceField(
        Investment.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False,
    )
    investment_stage = forms.ModelMultipleChoiceField(
        InvestmentStage.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False,
    )
    building = forms.ModelMultipleChoiceField(
        Building.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False,
    )
