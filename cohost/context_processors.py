# -*- coding: utf-8 *-*
from django.contrib.auth.models import User
from urllib2 import quote
from cohost.utils import get_client_ip



def common(request):
    user = request.user
    user_ip = get_client_ip(request)
    if not isinstance(user, User):
        return {}
    context = dict(
        USER_NAME=user.username,
        USER_IP=user_ip,
        )
    return context


def static(request):
    return dict(STATIC_URL=SETTINGS.STATIC_URL)
