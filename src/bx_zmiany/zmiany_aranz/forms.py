from django import forms

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
