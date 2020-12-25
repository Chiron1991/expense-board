import graphene
from django.contrib.auth import get_user_model
from graphene_django import DjangoObjectType

from expenses.models import CostCenter, Tag, VariableCost

_CURRENCY_SYMBOLS = {
    'EUR': '€',
    'USD': '$',
    'GBP': '£',
}


class MoneyType(graphene.ObjectType):
    """
    Used to represent moneyed's Money objects (as used by django-money's MoneyField).
    """
    amount = graphene.String()
    currencyName = graphene.String()
    currencyCode = graphene.String()
    currencySymbol = graphene.String()

    def resolve_amount(self, info):
        return str(self.amount)

    def resolve_currencyName(self, info):
        return self.currency.name

    def resolve_currencyCode(self, info):
        return self.currency.code

    def resolve_currencySymbol(self, info):
        return _CURRENCY_SYMBOLS.get(self.currency.code)


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'is_staff',
            'is_superuser',
        )


class TagType(DjangoObjectType):
    class Meta:
        model = Tag
        fields = ('title',)


class CostCenterType(DjangoObjectType):
    class Meta:
        model = CostCenter
        fields = ('name',)


class VariableCostType(DjangoObjectType):
    cost = graphene.Field(MoneyType)

    class Meta:
        model = VariableCost
        fields = ('date', 'cost', 'notes', 'cost_center', 'tags')
