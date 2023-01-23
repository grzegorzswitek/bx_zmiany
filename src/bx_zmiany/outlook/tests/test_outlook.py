import os
import logging
import tempfile
import win32com.client as win32


from django.test import TestCase
from django.core.exceptions import ValidationError

from outlook.outlook import Message
from outlook.models import Signature


logging.disable(logging.CRITICAL)


class OutlookApplicationTests(TestCase):
    def test_dispatch_outlook(self):
        try:
            win32.Dispatch("Outlook.Application")
        except Exception as e:
            raise Exception("Outlook.Application not found.") from e


class MessageTests(TestCase):
    def setUp(self):
        self.message = Message()

    def test_recipients_valid(self):
        self.message.to = ["User 11 <user@mail.com>", "User 12 <user2@mail.com>"]
        self.message.cc = ["User 21 <user@mail.com>", "User 22 <user2@mail.com>"]
        self.message.bcc = ["User 31 <user@mail.com>", "User 32 <user2@mail.com>"]
        self.assertEqual(
            self.message.to, ["User 11 <user@mail.com>", "User 12 <user2@mail.com>"]
        )
        self.assertEqual(
            self.message.cc, ["User 21 <user@mail.com>", "User 22 <user2@mail.com>"]
        )
        self.assertEqual(
            self.message.bcc, ["User 31 <user@mail.com>", "User 32 <user2@mail.com>"]
        )

    def test_recipients_invalid_address_format(self):
        with self.assertRaises(ValidationError):
            self.message.to = [
                "User 1 <user@mail.com>",
                "User 2 <user2.mail.com>",
            ]
        with self.assertRaises(ValidationError):
            self.message.cc = [
                "User 1 <user@mail.com>",
                "User 2 <user2.mail.com>",
            ]
        with self.assertRaises(ValidationError):
            self.message.bcc = [
                "User 1 <user@mail.com>",
                "User 2 <user2.mail.com>",
            ]

    def test_subject_valid(self):
        subject = "Subject of message"
        self.message.subject = subject
        self.assertEqual(self.message.subject, subject)

    def test_subject_invalid(self):
        with self.assertRaises(TypeError):
            self.message.subject = 123

    def test_body_valid(self):
        body = "Message body"
        self.message.body = body
        self.assertEqual(self.message.body, body)

    def test_body_invalid(self):
        with self.assertRaises(TypeError):
            self.message.body = 1

    def test_body_format_valid(self):
        for body_format in (0, 1, 2, 3):
            self.message.body_format = body_format
            self.assertEqual(self.message.body_format, body_format)

    def test_body_format_invalid_type(self):
        with self.assertRaises(TypeError):
            self.message.body_format = "1"

    def test_body_format_invalid_value(self):
        with self.assertRaises(ValueError):
            self.message.body_format = 4

    def test_attachments_valid(self):
        with tempfile.TemporaryFile() as f:
            with tempfile.TemporaryFile() as ff:
                path_1 = f.name
                path_2 = ff.name
                self.message.attachments = [path_1, path_2]
        self.assertEqual(self.message.attachments, [path_1, path_2])

    def test_attachments_type_error(self):
        with self.assertRaises(TypeError):
            with tempfile.TemporaryFile() as f:
                self.message.attachments = f.name

    def test_attachments_file_not_found_error(self):
        with self.assertRaises(FileNotFoundError):
            self.message.attachments = ["/non/valid/path"]

    def test_attachments_is_a_directory_eror(self):
        with self.assertRaises(IsADirectoryError):
            with tempfile.TemporaryDirectory() as d:
                self.message.attachments = [d]

    def test_default_signature_from_file(self):
        signature_content = "Best regards,\nGrzegorz Świtek"
        signature_file = tempfile.TemporaryFile(
            mode="w", encoding="UTF16", delete=False
        )
        signature_file.write(signature_content)
        signature_file.close()
        Signature.objects.create(name="default_signature", path=signature_file.name)
        # for body_format = 2 -> change \n to <br>
        self.message.body_format = 2
        self.message.signature = ""
        self.assertEqual(self.message.signature, "Best regards,<br>Grzegorz Świtek")
        # for body_format in (0, 1, 3) do nothing
        for body_format in (0, 1, 3):
            self.message.body_format = body_format
            self.message.signature = ""
            self.assertEqual(self.message.signature, signature_content)
        os.unlink(signature_file.name)

    def test_default_signature_from_text(self):
        signature_content = "Best regards,\nJan Kowalski"
        Signature.objects.create(
            name="default_signature_2", text=signature_content, default=True
        )
        # for body_format = 2 -> change \n to <br>
        self.message.body_format = 2
        self.message.signature = ""
        self.assertEqual(self.message.signature, "Best regards,<br>Jan Kowalski")
        # for body_format in (0, 1, 3) do nothing
        for body_format in (0, 1, 3):
            self.message.body_format = body_format
            self.message.signature = ""
            self.assertEqual(self.message.signature, signature_content)

    def test_correct_addresses(self):
        for field in ("to", "cc", "bcc"):
            value = ["user@example.com", "user2@example.com"]
            setattr(self.message, field, value)
            self.assertEqual(getattr(self.message, field), value)
            value = ["user@example.com", ""]
            setattr(self.message, field, value)
            self.assertEqual(getattr(self.message, field), value)
            value = [""]
            setattr(self.message, field, value)
            self.assertEqual(getattr(self.message, field), value)

    def test_incorrect_addresses(self):
        for field in ("to", "cc", "bcc"):
            with self.assertRaises(TypeError):
                value = "user@example.com"
                setattr(self.message, field, value)
            with self.assertRaises(TypeError):
                value = ["user@example.com", 123]
                setattr(self.message, field, value)
            with self.assertRaises(ValidationError):
                value = ["user.example.com"]
                setattr(self.message, field, value)

    def test_incorrect_body_format(self):
        for value in ("1", [], None, 1.0):
            with self.assertRaises(TypeError):
                self.message.body_format = value
        with self.assertRaises(ValueError):
            self.message.body_format = 4

    def test_add_signature(self):
        message_body_txt = "Test body message.\n"
        message_body_html = "<body>Test body message.<br>Second line.<br></body>"
        signature_content = "Best regards,\nJan Kowalski"
        expected_message_body_txt = "Test body message.Best regards,\nJan Kowalski"
        expected_message_body_html = "<body>Test body message.<br>Second line.<br>Best regards,<br>Jan Kowalski</body>"
        signature_name = "test"
        Signature.objects.create(
            name=signature_name,
            text=signature_content,
        )
        for body_format in (0, 1, 3):
            self.message.body = message_body_txt
            self.message.body_format = body_format
            self.message.signature = signature_name
            self.message._add_signature_to_body()
            self.assertEqual(self.message.body, expected_message_body_txt)
        for body_format in (2,):
            self.message.body = message_body_html
            self.message.body_format = body_format
            self.message.signature = signature_name
            self.message._add_signature_to_body()
            self.assertEqual(self.message.body, expected_message_body_html)
