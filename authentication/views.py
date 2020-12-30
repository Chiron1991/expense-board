from http import HTTPStatus

from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.debug import sensitive_post_parameters


class LoginView(View):
    @method_decorator(sensitive_post_parameters())
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, *args, **kwargs):
        auth_form = AuthenticationForm(self.request, data=self.request.POST)

        if auth_form.is_valid():
            username = auth_form.cleaned_data['username']
            password = auth_form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(self.request, user)
                return HttpResponse(status=HTTPStatus.CREATED)
            raise NotImplementedError(  # pragma: nocover
                f'No authentication backend returned a {get_user_model()._meta.model_name.title()} objects. '
                f'That should not have happened.'
            )

        return JsonResponse(auth_form.errors, status=HTTPStatus.BAD_REQUEST)


class LogoutView(View):
    def delete(self, request, *args, **kwargs):
        logout(request)
        return HttpResponse(status=HTTPStatus.NO_CONTENT)
