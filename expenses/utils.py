import functools

from django.urls import reverse
from django.utils.html import format_html


def related_object_link(func):
    """
    Decorator to wrap list_display getters on admin classes.
    It will take the decorated function's return value and display
    it as a link to the related object's edit site.
    """

    @functools.wraps(func)
    def wrapper(admin_instance, obj):
        display_text = func(admin_instance, obj)
        app_label = obj._meta.app_label
        model_name = obj._meta.model.__name__.lower()

        url = reverse(f'admin:{app_label}_{model_name}_change', args=[obj.id])

        return format_html('<a href="{}">{}</a>', url, display_text)

    return wrapper
