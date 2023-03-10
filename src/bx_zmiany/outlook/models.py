from django.db import models

from os import environ


def signature_path():
    user_profile = environ.get("userprofile")
    return f"{user_profile}\AppData\Roaming\Microsoft\Signatures"


class Signature(models.Model):
    """Model definition for Signature in message."""

    name = models.CharField(max_length=50, unique=True)
    path = models.FilePathField(
        path=signature_path(), match=".*\.txt", null=True, blank=True
    )
    text = models.TextField(null=True, blank=True)
    default = models.BooleanField(default=False)

    def save(self, *args, **kwargs) -> None:
        if self.default:
            signatures = Signature.objects.filter(default=True).exclude(pk=self.pk)
            for signature in signatures:
                signature.default = False
            Signature.objects.bulk_update(signatures, ["default"])
        else:
            if not Signature.objects.filter(default=True).exclude(pk=self.pk):
                self.default = True
        return super().save(*args, **kwargs)

    class Meta:
        """Meta definition for Signature."""

        verbose_name = "Signature"
        verbose_name_plural = "Signatures"

    def __str__(self):
        """Unicode representation of Signature."""
        return f"{self.name} {'(default)' if self.default else ''}".strip()

    def get_content(self):
        if self.path:
            try:
                with open(
                    self.path,
                    encoding="utf16",
                ) as f:
                    return f.read().strip()
            except FileNotFoundError:
                raise
        elif self.text:
            return self.text.strip()
        else:
            return ""
