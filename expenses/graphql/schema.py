import graphene

from expenses.graphql.object_types import TagType, CostCenterType, VariableCostType
from expenses.models import Tag, CostCenter, VariableCost


class Query(graphene.ObjectType):
    all_tags = graphene.List(TagType)
    all_cost_centers = graphene.List(CostCenterType)
    all_variable_expenses = graphene.List(VariableCostType)

    def resolve_all_tags(self, info):
        return Tag.objects.all()

    def resolve_all_cost_centers(self, info):
        return CostCenter.objects.all()

    def resolve_all_variable_expenses(self, info):
        return VariableCost.objects.all()


schema = graphene.Schema(query=Query)
