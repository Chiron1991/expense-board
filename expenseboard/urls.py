from django.conf import settings
from django.contrib import admin
from django.urls import include, path

from expenses.graphql.views import PrivateGraphQLView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('graphql/', PrivateGraphQLView.as_view(graphiql=settings.DEBUG)),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns.insert(0, path('__debug__/', include(debug_toolbar.urls)))
