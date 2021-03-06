import json

from django.http import HttpResponse
from django_sudo.utils import has_sudo_privileges
from functools import wraps


def sudo_required(func):
    @wraps(func)
    def wrapped(self, request, *args, **kwargs):
        if not has_sudo_privileges(request):
            # TODO(dcramer): support some kind of auth flow to allow this
            # externally
            data = {
                "error": "Account verification required.",
                "sudoRequired": True,
                "username": request.user.username,
            }
            return HttpResponse(json.dumps(data), status=401)
        return func(self, request, *args, **kwargs)
    return wrapped
