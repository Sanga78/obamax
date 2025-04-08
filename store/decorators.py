from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse
from functools import wraps
from django.core.exceptions import PermissionDenied

def superadmin_required(view_func):
    """Decorator to allow only superusers and staff (admins)"""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse('login'))
        if not (request.user.is_superuser or request.user.is_staff):
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def login_required_superadmin_required(view_func):
    """Combines login_required and superadmin_required"""
    return login_required(superadmin_required(view_func))