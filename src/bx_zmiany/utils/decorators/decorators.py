from functools import wraps


def ctx_menu_template(cls=None, *, template_name: str):
    """Set context['ctx_menu_template'] as template_name"""

    def decorator(cls):
        get_context_data = cls.get_context_data

        @wraps(cls.get_context_data)
        def updated_get_context_data(self, **kwargs):
            return get_context_data(self, ctx_menu_template=template_name, **kwargs)

        cls.get_context_data = updated_get_context_data
        return cls

    return decorator
