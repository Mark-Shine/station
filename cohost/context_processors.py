# -*- coding: utf-8 *-*
from django.contrib.auth.models import User
from urllib2 import quote


def common(request):
    user = request.user
    if not isinstance(user, User):
        return {}
    context = dict(
        USER_NAME=user.username,
        )
    return context


def static(request):
    return dict(STATIC_URL=SETTINGS.STATIC_URL)
