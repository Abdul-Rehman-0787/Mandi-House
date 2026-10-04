"""
Two levels of dashboard access:

- OWNER  = a superuser account (the restaurant owner). Can manage dishes,
  categories, deals, and add/remove staff accounts, in addition to orders.
- STAFF  = a plain staff account (is_staff=True, is_superuser=False),
  created by the owner. Can only view orders and update their status
  (i.e. confirm/complete/cancel by phone) — nothing else.
"""
from functools import wraps
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied


def owner_required(view_func):
    """Only the owner (superuser) may access this view."""
    @login_required(login_url="dashboard:owner_login")
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied("Only the restaurant owner can access this page.")
        return view_func(request, *args, **kwargs)
    return _wrapped


def staff_or_owner_required(view_func):
    """Any staff account (owner or regular staff) may access this view."""
    @login_required(login_url="dashboard:login")
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied("Staff access required.")
        return view_func(request, *args, **kwargs)
    return _wrapped
