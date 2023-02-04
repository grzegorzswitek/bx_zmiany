import re

from django.core.validators import validate_email


class EmailRecipientValidator:
    """Validate Recipient email address.

    Correct format:
        - 'User Name <user@example.com>'
        - 'user@example.com'
    """

    def __call__(self, value):
        recipient = value.strip()
        pattern = "<(.*)>$"
        if not recipient:
            return
        match = re.search(pattern, recipient)
        if match is None:
            email_address = recipient
        else:
            email_address = match.groups()[0]
        validate_email(email_address)
