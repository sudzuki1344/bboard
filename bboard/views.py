from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, Http404
from django.shortcuts import render
from django.template import loader
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import CreateView

from django import forms
from bboard.forms import BbForm
from bboard.models import Bb, Rubric
from django.db.models import Count


def index(request):
    # a = request.META
    # b = ""



    print(request.headers)
    print(request.META)
    print(request.META['CONTENT_TYPE'])
    print(request.META['HTTP_HOST'])
    print(request.META['HTTP_USER_AGENT'])
    print(request.resolver_match)


    bbs = Bb.objects.order_by('-published')
   # rubrics = Rubric.objects.all()
    rubrics = Rubric.objects.annotate(cnt=Count('bb')).filter(cnt__gt=0)
    context = {'bbs': bbs, 'rubrics': rubrics}

    return render(request, 'bboard/index.html', context)

# def index(request):
#     resp = HttpResponse(' Антанта', content_type='text/plain; charset=utf-8')
#     resp.write(' главная')
#     resp.writelines((' страница', ' сайта'))
#     resp['keywords'] = 'Python, Django'
#     return resp

# def index(request):
#     bbs = Bb.objects.all()
#     rubrics = Rubric.objects.all()
#     context = {'bbs': bbs, 'rubrics': rubrics}
#     from django.template.loader import get_template
#     template = get_template('bboard/index.html')
#     return HttpResponse(template.render(context, request))

# def index(requests):
#     bbs = Bb.objects.all()
#     rubrics = Rubric.objects.all()
#     context = {'bbs': bbs, 'rubrics': rubrics}
#     return HttpResponse(render_to_string('bboard/index.html', context, request))

def by_rubric(request, rubric_id):
    bbs = Bb.objects.filter(rubric=rubric_id)
    # rubrics = Rubric.objects.all()
    rubrics = Rubric.objects.annotate(cnt=Count('bb')).filter(cnt__gt=0)
    current_rubric = Rubric.objects.get(pk=rubric_id)

    # bbs = current_rubric.objects.all()

    context = {'bbs': bbs, 'rubrics': rubrics, 'current_rubric': current_rubric}

    return render(request, 'bboard/by_rubric.html', context)


class BbCreateView(CreateView):
    template_name = 'bboard/create.html'
    # form_class = BbForm
    success_url = reverse_lazy('bboard:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.annotate(cnt=Count('bb')).filter(cnt__gt=0)
        return context


def add(request):
    bbf = BbForm()
    context = {'form': bbf}
    return render(request, 'bboard/bb_create.html', context)

def add_save(request):
    bbf = BbForm(request.POST)
    if bbf.is_valid():
        bbf.save()
        return HttpResponseRedirect(reverse('bboard:by_rubric', kwargs={'rubric_id': bbf.cleaned_data['rubric'].pk}))
    else:
        context = {'form': bbf}
        return render(request, 'bboard/bb_create.html', context)

def add_and_save(request):

    for a in request.META:
        with open('1.txt', 'r') as file:
            file.write(str(a))

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('bboard:index'))
    if request.method == 'POST':
        bbf = BbForm(request.POST)
        if bbf.is_valid():
            bbf.save()
            return HttpResponseRedirect(reverse('bboard:by_rubric', kwargs={'rubric_id': bbf.cleaned_data['rubric'].pk}))
        else:
            context = {'form': bbf}
            return render(request, 'bboard/bb_create.html', context)
    else:
        bbf = BbForm()
        context = {'form': bbf}
        return render(request, 'bboard/bb_create.html', context)

def bb_detail(request, bb_id):
    try:
        bb = Bb.objects.get(pk=bb_id)
    except Bb.DoesNotExist:
        return Http404('Такое обьявлени не существует')

    rubrics = Rubric.objects.annotate(cnt=Count('bb')).filter(cnt__gt=0)
    context = {'bb': bb, 'rubrics': rubrics}

    return render(request, 'bboard/bb_detail.html', context)
