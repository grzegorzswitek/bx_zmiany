from django.forms import ModelForm
from django.forms.models import ModelChoiceField
from django.forms.widgets import Select, ChoiceWidget, Textarea
from django.contrib.admin import widgets as admin_widgets

from .models import CustomerOfProcedure, Customer
from .admin import CustomerAdmin
from .widgets import RelatedFieldWidgetWrapper


class CustomerOfProcedureForm(ModelForm):
    class Meta:
        model = CustomerOfProcedure
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["customer"].widget = RelatedFieldWidgetWrapper(
            Select(),
            Customer,
            "zmiany_aranz:customer_create",
            "zmiany_aranz:customer_update",
            "zmiany_aranz:customer_delete",
            can_add_related=True,
            can_change_related=True,
            can_delete_related=False,
        )
