from django import forms

from utils.validators import EmailRecipientValidator


class MultiEmailRecipientField(forms.Field):
    def __init__(self, *, delimiter="\r\n", **kwargs) -> None:
        super().__init__(**kwargs)
        self.delimiter = delimiter

    def to_python(self, value):
        """Normalize data to a list of strings."""
        # Return an empty list if no input was given.
        if not value:
            return []
        return [email.strip() for email in value.split(self.delimiter) if email]

    def validate(self, value):
        """Check if value consists only of valid emails."""
        super().validate(value)
        v = EmailRecipientValidator()
        for recipient in value:
            v(recipient)
