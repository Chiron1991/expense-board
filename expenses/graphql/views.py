from graphene_django.views import GraphQLView

from expenses.utils import AuthenticationRequiredMixin


class PrivateGraphQLView(AuthenticationRequiredMixin, GraphQLView):
    """
    Like django_graphene's GraphQLView, but requires authentication to access.
    """
