#encoding=utf-8
import json
from django.utils import timezone
from django.contrib.auth.hashers import check_password
from django.db import connection
from django.utils.timezone import utc
from django.shortcuts import render
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import loader
from django.template.context import (Context, RequestContext)
from django.utils.safestring import mark_safe
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.core.urlresolvers import reverse
from django.forms.models import model_to_dict
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
# Create your views here.
from .utils import encrypt_password, validate_password

from auth.forms import AccountForm


class LoginView(View):
    template_name = 'login.html'

    def get(self, request):
        # request_context = RequestContext(request, {})
        page = render(request, self.template_name, {})
        return HttpResponse(page)
        
    def post(self, request):
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('home'))
                    # Redirect to a success page.
                else:
                    return HttpResponse("disabled account")
                    # Return a 'disabled account' error message
            else:
                # Return an 'invalid login' error message.
                return HttpResponseRedirect(reverse('login'))
        return HttpResponse("error")


def logoff(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))





