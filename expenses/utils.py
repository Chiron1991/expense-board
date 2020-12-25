import functools
import json
import pprint
import sys
from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.test import Client, TestCase
from django.urls import reverse
from django.utils.html import format_html
from graphene_django.utils.testing import graphql_query


def prettify(obj, stream=sys.stdout, **format_kwargs):
    """
    Writes an object to the given stream (stdout by default) in a nicely formatted way.
    Prettifying is attempted by JSON-encoding the object, or using the pprint module as a fallback.
    """
    format_kwargs.setdefault('indent', 4)
    format_kwargs.setdefault('sort_keys', True)

    try:
        stream.write(json.dumps(obj, cls=DjangoJSONEncoder, **format_kwargs))
    except Exception:
        return pprint.pprint(obj, stream=stream, width=120)


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


class AuthenticationRequiredMixin:
    """
    Can be mixed into CBVs and will return HTTP 401 if the user is not authenticated.
    """

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponse(status=HTTPStatus.UNAUTHORIZED)
        return super().dispatch(request, *args, **kwargs)


class GraphQLTestCase(TestCase):
    """
    Base class for testing this project's GraphQL API.
    """

    def setUp(self):
        self.superuser = get_user_model().objects.create_superuser(username='root', password='root')
        self.user = get_user_model().objects.create_user(username='john', password='john')

        self.client = Client()

        super().setUp()

    def query(self, query, user=None, **kwargs):
        if user is not None:
            self.client.login(username=user.username, password=user.username)

        response = graphql_query(
            query,
            client=self.client,
            graphql_url='/graphql/',
            **kwargs,
        )

        if user is not None:
            self.client.logout()

        return response
