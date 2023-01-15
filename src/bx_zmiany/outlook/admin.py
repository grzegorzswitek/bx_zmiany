from django.contrib import admin, messages

from .models import Signature


class SignatureAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        default_before = True if request.POST.get("default") else False
        super(SignatureAdmin, self).save_model(request, obj, form, change)
        if not default_before == obj.default:
            messages.add_message(
                request,
                messages.WARNING,
                f"Field 'default' has been changed to '{obj.default}'",
            )


admin.site.register(Signature, SignatureAdmin)
