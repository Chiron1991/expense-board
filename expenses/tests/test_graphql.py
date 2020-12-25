import json
from http import HTTPStatus

import graphene
from django.test import TestCase
from moneyed import Money

from expenses.graphql.object_types import MoneyType, _CURRENCY_SYMBOLS
from expenses.utils import GraphQLTestCase


class ObjectTypeTestCase(TestCase):
    class MoneyTypeTestQuery(graphene.ObjectType):
        regular = graphene.Field(MoneyType)
        currencyWithNoCurrencySymbol = graphene.Field(MoneyType)

        def resolve_regular(self, info):
            return Money('10.0', 'USD')

        def resolve_currencyWithNoCurrencySymbol(self, info):
            unknown_currency = 'FKP'  # Falkland Islands Pound
            assert unknown_currency not in _CURRENCY_SYMBOLS
            return Money('10.0', unknown_currency)

    def test_money_type(self):
        schema = graphene.Schema(query=self.MoneyTypeTestQuery)
        all_fields = ' '.join(('amount', 'currencyName', 'currencyCode', 'currencySymbol'))
        query = 'query { regular { ' + all_fields + ' } currencyWithNoCurrencySymbol { ' + all_fields + ' } }'
        result = schema.execute(query)

        self.assertIsNone(result.errors)
        self.assertFalse(result.invalid)

        self.assertDictEqual(result.data['regular'], {
            'amount': '10.0',
            'currencyName': 'US Dollar',
            'currencyCode': 'USD',
            'currencySymbol': '$',
        })
        self.assertDictEqual(result.data['currencyWithNoCurrencySymbol'], {
            'amount': '10.0',
            'currencyName': 'Falkland Islands Pound',
            'currencyCode': 'FKP',
            'currencySymbol': None,
        })


class SchemaTestCase(GraphQLTestCase):
    def test_authentication_required(self):
        response = self.query('query { me { id } }', user=None)
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

    def test_me_query(self):
        me_fields = ' '.join((
            'id',
            'username',
            'firstName',
            'lastName',
            'email',
            'isStaff',
            'isSuperuser',
        ))
        response = self.query('query { me { ' + me_fields + ' } }', user=self.user)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        content = json.loads(response.content)
        self.assertNotIn('errors', content)
        self.assertDictEqual(content['data']['me'], {
            'id': str(self.user.id),
            'username': self.user.username,
            'firstName': self.user.first_name,
            'lastName': self.user.last_name,
            'email': self.user.email,
            'isStaff': self.user.is_staff,
            'isSuperuser': self.user.is_superuser,
        })
