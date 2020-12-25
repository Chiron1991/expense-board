import graphene

from expenses.graphql.object_types import CostCenterType, TagType, UserType, VariableCostType
from expenses.models import CostCenter, Tag, VariableCost


class Query(graphene.ObjectType):
    me = graphene.Field(UserType)
    all_tags = graphene.List(TagType)
    all_cost_centers = graphene.List(CostCenterType)
    all_variable_expenses = graphene.List(VariableCostType)

    def resolve_me(self, info):
        return info.context.user

    def resolve_all_tags(self, info):
        return Tag.objects.all()

    def resolve_all_cost_centers(self, info):
        return CostCenter.objects.all()

    def resolve_all_variable_expenses(self, info):
        return VariableCost.objects.all()


schema = graphene.Schema(query=Query)
