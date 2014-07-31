import math

from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.core.urlresolvers import reverse
from django.template.context import (Context, RequestContext)
from django.template.loader import Template
from django.core.paginator import Paginator
from django.template.response import TemplateResponse

from cohost.models import Data
from cohost.models import Keywords
from cohost.models import Cate

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
    paged_objects = paginate(objects, pagenum)
    pagination = render_to_string('pagination.html', {
        'page_count': range(1, int(paged_objects.page_count)+1),
        'objects':paged_objects,
        'loop_times':range(1,6)},
        context_instance=RequestContext(request))
    return paged_objects, pagination

def build_pages(model,):
    def wrraped(show_func):
        def _page(request, **kwargs):
            pagenum = request.GET.get("page", 1)
            objecs = model.objects.all()
            paged_objects, pagination = get_pagination(request, objecs, int(pagenum))
            context = {}
            context['pagination'] = pagination
            context['objects'] = paged_objects
            r = show_func(request)
            r.context_data.update(context) 
            result = r.render()
            return result
        return _page
    return wrraped

@build_pages(model=Keywords)
def show_kwords(request):
    context = {}
    context['keyword_active'] = "active"
    return TemplateResponse(request, 'cohost/keywords.html', context)

@build_pages(model=Data)
def show_data(request):
    context = {}
    context['data_active'] = "active"
    return TemplateResponse(request, "cohost/data.html", context)




# def show_kwords(request):
#     context = Context()
#     keys = Keywords.objects.all()
#     context['keys'] = keys
#     context['keyword_active'] = "active"
#     page = render_to_string("cohost/keywords.html", context, context_instance=RequestContext(request, {}))
#     return HttpResponse(page)

# def show_data(request):
#     pagenum = request.GET.get("page", 1)
#     datas = Data.objects.all()
#     paged_objects, pagination = get_pagination(request, datas, int(pagenum))
#     context = Context()
#     context['pagination'] = pagination
#     context['datas'] = paged_objects
#     context['data_active'] = "active"
#     page = render(request, "cohost/data.html", context)
#     return HttpResponse(page)







