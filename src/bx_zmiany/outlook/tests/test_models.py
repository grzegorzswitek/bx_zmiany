import os
import tempfile

from django.urls import reverse
from django.test import TestCase

from outlook.models import Signature


class SignatureTests(TestCase):
    def setUp(self):
        self.object = Signature.objects.create(name="default_signature")
        self.signature_content = "Best regards,\nGrzegorz Świtek"

    def test_get_content_from_file(self):
        signature_file = tempfile.TemporaryFile(
            mode="w", encoding="UTF16", delete=False
        )
        signature_file.write(self.signature_content)
        signature_file.close()
        self.object.path = signature_file.name
        self.object.save()
        self.assertEqual(self.object.get_content(), self.signature_content)
        os.unlink(signature_file.name)

    def test_get_content_from_text(self):
        self.object.text = self.signature_content
        self.object.save()
        self.assertEqual(self.object.get_content(), self.signature_content)
