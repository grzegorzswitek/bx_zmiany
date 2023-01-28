import re

from django import forms
from django.core.validators import validate_email


class SendEmailForm(forms.Form):
    """Send Email form definition."""

    class RecipientValidator:
        """Verifies that the recipient fields [to, cc, bcc]
        contain a valid email address."""

        def __call__(self, value):
            recipients = value.strip().split("\r\n")
            pattern = "<(.*)>"
            for recipient in recipients:
                if not recipient:
                    continue
                match = re.search(pattern, recipient)
                if match is None:
                    email_address = recipient
                else:
                    email_address = match.groups()[0]
                validate_email(email_address)

    to = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"rows": 5}),
        validators=[RecipientValidator()],
    )
    cc = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"rows": 5}),
        validators=[RecipientValidator()],
    )
    bcc = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"rows": 5}),
        validators=[RecipientValidator()],
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

    def clean(self):
        data = super().clean()
        # Change the recipient's TextField values to lists
        for field in ("to", "cc", "bcc"):
            data[field] = data.get(field, "").strip().split("\r\n")
        return data
