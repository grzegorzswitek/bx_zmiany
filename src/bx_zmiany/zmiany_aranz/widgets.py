import copy

from django import forms
from django.db.models import CASCADE
from django.urls import reverse


class RelatedFieldWidgetWrapper(forms.Widget):
    """
    This class is a wrapper to a given widget to add the add icon for the
    admin interface.
    """

    template_name = "admin/widgets/related_widget_wrapper.html"

    def __init__(
        self,
        widget,
        rel,
        add_related_url,
        change_related_url,
        delete_related_url,
        can_add_related=None,
        can_change_related=False,
        can_delete_related=False,
        can_view_related=False,
    ):
        self.needs_multipart_form = widget.needs_multipart_form
        self.attrs = widget.attrs
        self.choices = widget.choices
        self.widget = widget
        self.rel = rel
        # Backwards compatible check for whether a user can add related
        # objects.
        self.can_add_related = can_add_related
        # XXX: The UX does not support multiple selected values.
        multiple = getattr(widget, "allow_multiple_selected", False)
        self.can_change_related = not multiple and can_change_related
        # XXX: The deletion UX can be confusing when dealing with cascading deletion.
        cascade = getattr(rel, "on_delete", None) is CASCADE
        self.can_delete_related = not multiple and not cascade and can_delete_related
        self.can_view_related = not multiple and can_view_related
        # so we can check if the related object is registered with this AdminSite
        self.add_related_url = add_related_url
        self.change_related_url = change_related_url
        self.delete_related_url = delete_related_url

    def __deepcopy__(self, memo):
        obj = copy.copy(self)
        obj.widget = copy.deepcopy(self.widget, memo)
        obj.attrs = self.widget.attrs
        memo[id(self)] = obj
        return obj

    @property
    def is_hidden(self):
        return self.widget.is_hidden

    @property
    def media(self):
        return self.widget.media

    def get_related_url(self, url_name, *args):
        return reverse(url_name, args=args)

    def get_context(self, name, value, attrs):
        from django.contrib.admin.views.main import IS_POPUP_VAR, TO_FIELD_VAR

        self.widget.choices = self.choices
        url_params = "&".join(
            "%s=%s" % param
            for param in [
                (TO_FIELD_VAR, self.rel._meta.pk.name),
                (IS_POPUP_VAR, 1),
            ]
        )
        context = {
            "rendered_widget": self.widget.render(name, value, attrs),
            "is_hidden": self.is_hidden,
            "name": name,
            "url_params": url_params,
            "model": self.rel._meta.verbose_name,
            "can_add_related": self.can_add_related,
            "can_change_related": self.can_change_related,
            "can_delete_related": self.can_delete_related,
            "can_view_related": self.can_view_related,
        }
        if self.can_add_related:
            context["add_related_url"] = self.get_related_url(self.add_related_url)
        if self.can_delete_related:
            context["delete_related_template_url"] = self.get_related_url(
                self.delete_related_url, "__fk__"
            )
        if self.can_view_related or self.can_change_related:
            context["change_related_template_url"] = self.get_related_url(
                self.change_related_url, "__fk__"
            )
        return context

    def value_from_datadict(self, data, files, name):
        return self.widget.value_from_datadict(data, files, name)

    def value_omitted_from_data(self, data, files, name):
        return self.widget.value_omitted_from_data(data, files, name)

    def id_for_label(self, id_):
        return self.widget.id_for_label(id_)
