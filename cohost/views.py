#encoding=utf-8
import math
import time
import operator
import datetime

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.template.context import (Context, RequestContext)
from django.template.loader import Template
from django.core.paginator import Paginator
from django.template.response import TemplateResponse
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.utils import timezone

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from cohost.models import Data
from cohost.models import Keywords
from cohost.models import Cate
from cohost.models import Area
from cohost.forms import DataStateForm, AreaForm
from cohost.models import STATE_CHOICES
from cohost.models import Ippiece
from wzauth.models import WzUser
from cohost.signals import action_message
from cohost.models import DataActionRecord


PAGE_SIZE = 10

def page(objects, num):
    paginator = Paginator(objects, PAGE_SIZE)
    num = paginator.num_pages if num > paginator.num_pages else num
    objects = paginator.page(num)
    return objects

def paginate(objects_query, pagenum):
    """paginate objetcs"""
    object_count = objects_query.count()
    page_count = int(math.ceil(1.0 * object_count / PAGE_SIZE))
    page_count = max(page_count, 1)
    paged_objects = page(objects_query, pagenum)
    paged_objects.page_count = page_count
    return paged_objects

# Create your views here.
def get_pagination(request, objects, pagenum=1):
    #查询的页面
    icpno = request.GET.get("icpno",)
    cate = request.GET.get("cate")
    state = request.GET.get("state")
    ip = request.GET.get("ip")
    queryurl = "cate=%s&ip=%s&state=%s&icpno=%s" % (cate, ip, state, icpno)

    paged_objects = paginate(objects, pagenum)
    pagination = render_to_string('pagination.html', {
        'queryurl': queryurl, 
        'page_count': range(1, int(paged_objects.page_count)+1),
        'objects':paged_objects,
        'loop_times': range(1,6)},
        context_instance=RequestContext(request))
    return paged_objects, pagination

def build_pages(model, condition=None):
    def wrraped(show_func):
        def _page(request, **kwargs):
            pagenum = request.GET.get("page", 1)
            if condition is None:
                objs = model.objects.all()
            else:
                objs = model.objects.filter(condition)
            r = show_func(request)
            #外围过滤条件
            Qs = r.context_data.get("q", "")
            if Qs:
                objs = objs.filter(Qs)
            paged_objects, pagination = get_pagination(request, objs, int(pagenum))
            context = {}
            context['pagination'] = pagination
            context['objects'] = paged_objects
            r.context_data.update(context) 
            result = r.render()
            return result
        return _page
    return wrraped

@login_required
def show_ips(request):
    pagenum = request.GET.get("page", 1)
    context = {}
    context['ips_active'] = "active"
    ips = Data.objects.all().values_list('ip', flat=True).distinct()
    context['total_count'] = ips.count()
    paged_objects, pagination = get_pagination(request, ips, int(pagenum))
    context['pagination'] = pagination
    context['objects'] = paged_objects  
    return render(request, 'cohost/ips.html', context)


@login_required
@build_pages(model=Keywords)
def show_kwords(request):
    context = {}
    context['keyword_active'] = "active"
    return TemplateResponse(request, 'cohost/keywords.html', context)


@login_required
@build_pages(model=Data, condition=~Q(state="-1"))
def show_data(request):
    user = request.user

    icpno = request.GET.get("icpno",)
    cate = request.GET.get("cate")
    state = request.GET.get("state")
    ip = request.GET.get("ip")
    #处理iP查询
    icp_q = None
    if icpno:
        icp_q = ("icpno__isnull", True) if icpno == '0' else ("icpno__isnull", False)
    predicates = [cate and ("cate",  int(cate)), state and ("state", state), ip and ("ip__startswith", ip)]
    if icp_q:
        predicates.append(icp_q)
    
    #获取用户的管辖区域
    if not user.is_superuser:
        wzuser = WzUser.objects.get(user=user)
        user_areas = wzuser.area.all()
        predicates.append(("area__in", user_areas))
    
    #将所有的查询条件生成Q()对象
    qs = [Q(x) for x in predicates if x]
    context = {}
    filter_context = {}
    filter_context['cates'] = Cate.objects.all()
    filter_context['states'] = STATE_CHOICES
    filter_context.update(request.GET.dict())
    data_counts = Data.objects.filter(reduce(operator.and_, qs, Q())).filter(~Q(state="-1")).count()
    filter_context['data_counts'] = data_counts
    #Q()是必须的，否则当所有条件为空会报错
    context['q'] = reduce(operator.and_, qs, Q())
    context['data_counts'] = data_counts
    context['filter_section'] = render_to_string("include/filter_section.html", filter_context)
    context['data_active'] = "active"
    return TemplateResponse(request, "cohost/data.html", context)

@login_required
def show_data_detail(request, pk):
    template = "cohost/detail.html"
    context = {}
    _object = get_object_or_404(Data, id=pk)
    context['object'] = _object
    context['data_active'] = "active"
    return render(request, template, context)



@login_required
def edit_data(request, pk):
    template = "cohost/edit_data.html"
    context = {}
    _object = get_object_or_404(Data, id=pk)
    context['object'] = _object
    form = DataStateForm(initial={
        'state': _object.state, 
        "cate": _object.cate,
        "related_law":_object.related_law})
    form.helper.form_action = reverse("change_detail", args=[pk])
    context['data_active'] = "active"
    context['form'] = form
    return render(request, template, context)


@login_required
def change_detail(request, pk):
    user = request.user
    form = DataStateForm(request.POST)
    if form.is_valid():
        cleaned_data = form.cleaned_data
        queryset = Data.objects.filter(id=pk)
        queryset.update(**cleaned_data)
        obj = queryset[0]
        try:
            action_message.send(sender=Data.__class__, 
                user=user, 
                instance=obj,
                action=u"处理记录",)
        except Exception, e:
            raise e
        status = 1
    next = reverse("data")
    return HttpResponseRedirect(next)


@login_required
def search_ip(request):
    template = "cohost/ip.html"
    curIP = request.GET.get("ip")
    queryset = Data.objects.filter(ip=curIP)
    context = {}
    context['objects'] = queryset if queryset.exists() else None
    context['ips_active'] = "active"
    return render(request, template, context)

@build_pages(model=Area)
def show_areas(request):
    context = {}
    context['area_active'] = "active"
    return TemplateResponse(request, "cohost/areas.html", context)

@login_required
def show_logs(request):
    pagenum = request.GET.get("page", 1)
    context = {}
    context['logs_active'] = "active"
    objs = DataActionRecord.objects.all().order_by("-time")
    paged_objects, pagination = get_pagination(request, objs, int(pagenum))
    context['pagination'] = pagination  
    context['objects'] = paged_objects
    return render(request, "cohost/logs.html", context)

def manage_area(request):
    action = request.POST.get('action')
    if action == "create":
        area = request.POST.get("area")
        form = AreaForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            area_obj =  Area.objects.get(id=int(area))
            piece = cleaned_data.pop('ip_piece')
            cleaned_data['area'] = area_obj
            cleaned_data['piece'] = piece
            Ippiece.objects.create(**cleaned_data)
            Data.objects.filter(~Q(state="-1")).filter(ip__startswith=piece).update(area=area_obj)

    elif action == "delete":
        pk = request.POST.get("id")
        quertset = Ippiece.objects.filter(pk=pk)
        if quertset.exists():
            #处理data对应area
            Data.objects.filter(~Q(state="-1")).filter(ip__startswith=quertset[0].piece, area=quertset[0].area).update(area=None)
            quertset.delete()


    return HttpResponseRedirect(reverse("areas"))

@login_required 
def show_result(request):
    """提示页面"""
    context = {}
    template = "result.html"
    next = request.GET.get('next')
    status = request.GET.get('status')
    context['next'] = next
    if status=="1":
        message = u"成功"
    else:
        message = u"失败"
    context['status'] = status
    context['message'] = message
    context['style'] = "success" if status=='1' else "warning"
    return render(request, template, context)


@login_required
def show_home(request):
    template = "cohost/home.html"
    datas = Data.objects.filter(~Q(state="-1")).count()
    ips = Data.objects.all().values_list('ip', flat=True).distinct().count()
    areas = Area.objects.all().count()
    cts, states, is_beians = count_for_data()
    context = {}
    context['home_active'] = 'active'
    context.update(**locals())
    return render(request, template, context)

def count_for_data():
    cates = Cate.objects.all()
    #分类
    cts = []
    for c in cates:
        cts.append({'name': c.name, "counts": c.data_set.all().count()})
    #状态统计
    data_set = Data.objects.filter(~Q(state="-1"))
    states = []
    for state, sname in iter(STATE_CHOICES):
        states.append({"counts": data_set.filter(state=state).count(), "name": sname})
    is_beians = []

    is_beians.append({"counts": data_set.filter(icpno=None).count(), "name": u"未备案"})
    is_beians.append({"counts": data_set.exclude(icpno=None).count(), "name": u"已备案"})
    return cts, states, is_beians
        






