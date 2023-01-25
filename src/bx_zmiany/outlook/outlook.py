from typing import *
from os import path
import logging

import win32com.client as win32

from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from .models import Signature

logging.basicConfig(level=logging.INFO)


class Message:
    def __init__(
        self,
        to: List[str] = [],
        cc: List[str] = [],
        bcc: List[str] = [],
        subject: str = "",
        body: str = "",
        body_format: int = 2,
        attachments: list = [],
        signature_name: str = "",
    ) -> None:
        """Initialize Message instance

        Args:
            to (List[str], optional): list of to recipients ["John Doe <user@example.com>", ...].
            cc (List[str], optional): list of cc recipients ["John Doe <user@example.com>", ...].
            bcc (List[str], optional): list of bcc recipients ["John Doe <user@example.com>", ...].
            subject (str, optional): Message subject. Defaults to "".
            body (str, optional): Message body. Defaults to "".
            body_format (int, optional): Format of message body
                0: Unspecified,
                1: Plain,
                2: HTML,
                3: Rich text.
            attachments (list, optional): List of attachments path. Defaults to [].
        """
        self.to = to
        self.cc = cc
        self.bcc = bcc
        self.subject = subject
        self.body_format = body_format
        self.body = body
        self.attachments = attachments
        self.signature = signature_name

    def _validate_recipients(self, recipients):
        """Checks if the recipients are defined as a list of str
        and if the e-mail address format is correct."""
        if not isinstance(recipients, list):
            raise TypeError(f"argument must be a list, not {type(recipients).__name__}")
        if not recipients:
            return []
        if not all([isinstance(recipient, str) for recipient in recipients]):
            raise TypeError("recipient must be a str")

        import re

        pattern = "<(.*)>"
        for recipient in recipients:
            match = re.search(pattern, recipient)
            if match is None:
                email_address = recipient
            else:
                email_address = match.groups()[0]
            if not email_address:
                continue
            try:
                validate_email(email_address)
            except ValidationError as e:
                raise ValidationError(f"Bad e-mail address: {email_address!r}.") from e
        return recipients

    @property
    def to(self):
        return self.__to

    @to.setter
    def to(self, recipients):
        self.__to = self._validate_recipients(recipients)

    @property
    def cc(self):
        return self.__cc

    @cc.setter
    def cc(self, recipients):
        self.__cc = self._validate_recipients(recipients)

    @property
    def bcc(self):
        return self.__bcc

    @bcc.setter
    def bcc(self, recipients):
        self.__bcc = self._validate_recipients(recipients)

    @property
    def subject(self):
        return self.__subject

    @subject.setter
    def subject(self, subject):
        """Sets a 'subject' parameter. Subject must be less than 79 characters."""
        if not isinstance(subject, str):
            raise TypeError(
                f"'subject' argument must be a str, not {type(subject).__name__}"
            )
        subject = subject.strip()
        if len(subject) > 78:
            raise ValueError("'subject' argument is too long. Max length is 77.")
        self.__subject = subject

    @property
    def body(self):
        return self.__body

    @body.setter
    def body(self, body):
        if not isinstance(body, str):
            raise TypeError(f"'body' argument must be a str, not {type(body).__name__}")
        if self.body_format == 2:
            body = body.replace("\r\n", "<br>").replace("\n", "<br>")
        self.__body = body

    @property
    def body_format(self):
        return self.__body_format

    @body_format.setter
    def body_format(self, body_format):
        if not isinstance(body_format, int):
            raise TypeError(
                f"'body_format' argument must be a int, not {type(body_format).__name__}"
            )
        if not body_format in (0, 1, 2, 3):
            raise ValueError(
                f"'body_format' argument must be in (0, 1, 2, 3), not {body_format}"
            )
        self.__body_format = body_format
        if body_format == 2 and hasattr(self, "body"):
            self.body = self.body.replace("\r\n", "<br>").replace("\n", "<br>")
        elif hasattr(self, "body"):
            self.body = self.body.replace("<br>", "\r\n")

    @property
    def attachments(self):
        return self.__attachments

    @attachments.setter
    def attachments(self, attachments):
        if not isinstance(attachments, list):
            raise TypeError(
                f"'attachments' argument must be a list, not {type(attachments).__name__}"
            )
        for attachment in attachments:
            if not path.exists(attachment):
                raise FileNotFoundError(f"Not found: {attachment}.")
            if path.isdir(attachment):
                raise IsADirectoryError(
                    f"File expected, directory received: {attachment}"
                )
        self.__attachments = attachments

    @property
    def signature(self):
        return self.__signature

    @signature.setter
    def signature(self, signature_name):
        if not isinstance(signature_name, str):
            raise TypeError(
                f"'signature_name' argument must be a str, not {type(signature_name).__name__}."
            )
        if signature_name:
            try:
                signature_obj = Signature.objects.get(name=signature_name)
                logging.info(f"Znaleziono podpis '{signature_name}'")
            except Signature.DoesNotExist:
                logging.warning("Nie znaleziono obiektu")
                self.__signature = ""
                return
        else:
            try:
                signature_obj = Signature.objects.get(default=True)
                logging.info(f"Znaleziono podpis domyślny")
            except Signature.DoesNotExist:
                logging.warning("Brak domyślnego obiektu")
                self.__signature = ""
                return
        try:
            self.__signature = signature_obj.get_content()
        except:
            logging.warning("Message.get_content() was failed.")
            self.__signature = ""
            return

        if self.body_format == 2:
            self.__signature = self.__signature.replace("\r\n", "<br>").replace(
                "\n", "<br>"
            )

    def _add_signature_to_body(self):
        if not self.signature:
            return
        index = self.body.find("</body>")
        if index > 0:
            self.body = self.body[:index] + self.signature + self.body[index:]
        else:
            self.body = self.body.strip() + f"{self.signature}"

    def create(self):
        """Create an e-mail instance but not display."""
        outlook: win32.CDispatch = win32.Dispatch("Outlook.Application")
        mail_item = outlook.CreateItem(0)
        mail_item.To = ";".join(self.to)
        mail_item.CC = ";".join(self.cc)
        mail_item.BCC = ";".join(self.bcc)
        mail_item.Subject = self.subject
        self._add_signature_to_body()
        if self.body_format == 2:
            mail_item.HTMLBody = self.body
        else:
            mail_item.Body = self.body
        mail_item.BodyFormat = self.body_format
        for attachment in self.attachments:
            mail_item.Attachments.Add(attachment)
        self._mail_item = mail_item

    def display(self):
        """Display an e-mail instance."""
        self._mail_item.Display()
