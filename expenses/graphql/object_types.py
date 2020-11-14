from graphene_django import DjangoObjectType

from expenses.models import Tag, CostCenter, VariableCost


class TagType(DjangoObjectType):
    class Meta:
        model = Tag


class CostCenterType(DjangoObjectType):
    class Meta:
        model = CostCenter


class VariableCostType(DjangoObjectType):
    class Meta:
        model = VariableCost
