import win32com.client as win32
from typing import *
from os import path
import traceback
import sys

from django.core.exceptions import ValidationError
from django.core.validators import validate_email

outlook: win32.CDispatch = win32.Dispatch(
    "Outlook.Application"
)  # .GetNamespace("MAPI") ??


class Message:
    def __init__(
        self,
        to: List[Tuple[str, str]] = [],
        cc: List[Tuple[str, str]] = [],
        bcc: List[Tuple[str, str]] = [],
        subject: str = "",
        body: str = "",
        body_format: int = 2,
        attachments: list = [],
    ) -> None:
        """Initialize Message instance

        Args:
            to (List[Tuple[str, str, str]], optional): list of to recipients tuple [(name, email), (...)].
            cc (List[Tuple[str, str, str]], optional): list of cc recipients tuple [(name, email), (...)].
            bcc (List[Tuple[str, str, str]], optional): list of bcc recipients tuple [(name, email), (...)].
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
        self.body = body
        self.body_format = body_format
        self.attachments = attachments

    def _validate_recipients(self, recipients):
        if not isinstance(recipients, list):
            raise TypeError(f"argument must be a list, not {type(recipients).__name__}")
        if not recipients:
            return
        for recipient in recipients:
            if not [type(field) for field in recipient] == [str, str]:
                raise TypeError("recipient must be a tuple of str")
            *_, email_address = recipient
            try:
                validate_email(email_address)
            except ValidationError as e:
                raise ValidationError(f"Bad e-mail address: {email_address}.") from e

    def _make_recipients(self, recipients):
        self._validate_recipients(recipients)
        result = []
        for recipient in recipients:
            name, e_mail = recipient
            result.append(f"{name}<{e_mail}>".strip())
        return result

    @property
    def to(self):
        return self.__to

    @to.setter
    def to(self, recipients):
        self.__to = self._make_recipients(recipients)

    @property
    def cc(self):
        return self.__cc

    @cc.setter
    def cc(self, recipients):
        self.__cc = self._make_recipients(recipients)

    @property
    def bcc(self):
        return self.__bcc

    @bcc.setter
    def bcc(self, recipients):
        self.__bcc = self._make_recipients(recipients)

    @property
    def subject(self):
        return self.__subject

    @subject.setter
    def subject(self, subject):
        if not isinstance(subject, str):
            raise TypeError(
                f"'subject' argument must be a str, not {type(subject).__name__}"
            )
        subject = subject.strip()
        if len(subject) > 78:
            raise ValueError("'subject' argument is too long.")
        self.__subject = subject

    @property
    def body(self):
        return self.__body

    @body.setter
    def body(self, body):
        if not isinstance(body, str):
            raise TypeError(f"'body' argument must be a str, not {type(body).__name__}")
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

    def _get_signature(self):
        pass

    def create(self):
        mail_item = outlook.CreateItem(0)
        mail_item.To = ";".join(self.to)
        mail_item.CC = ";".join(self.cc)
        mail_item.BCC = ";".join(self.bcc)
        mail_item.Subject = self.subject
        if self.body_format == 2:
            mail_item.HTMLBody = self.body
        else:
            mail_item.Body = self.body
        mail_item.BodyFormat = self.body_format
        for attachment in self.attachments:
            mail_item.Attachments.Add(attachment)
        self._mail_item = mail_item

    def display(self):
        self._mail_item.Display()


def main():
    mess = Message(
        [("Grzegorz Świtek", "switek.budlex.pl")],
        [("Grzegorz Świtek", "switek@gmail.com")],
        [("Grzegorz Świtek", "switek@o2.pl")],
        "Temat",
        "<b>Treść wiadomości</b>",
        2,
        [
            r"D:\Users\gswitek\Documents\01 ZMIANY\Dan  e Klienta.pdf",
            r"D:\Users\gswitek\Documents\01 ZMIANY\Instrukcja wprowadzania zmian aranżacyjnych - Olsztyn.pdf",
        ],
    )
    mess.create()
    mess.display()


if __name__ == "__main__":
    # main()
    print(type(outlook))
