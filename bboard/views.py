from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, Http404, StreamingHttpResponse, \
    FileResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.template import loader
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.views.decorators.http import require_http_methods, require_GET, require_POST, require_safe
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, FormView, UpdateView, DeleteView
from django.views.generic.base import View, TemplateView

from django import forms
from bboard.forms import BbForm
from bboard.models import Bb, Rubric
from django.db.models import Count

def index(request):
    bbs = Bb.objects.order_by('-published')
   # rubrics = Rubric.objects.all()
    rubrics = Rubric.objects.annotate(cnt=Count('bb')).filter(cnt__gt=0)
    context = {'bbs': bbs, 'rubrics': rubrics}

    return render(request, 'bboard/index.html', context)

class Index1(TemplateView):
    template_name = 'bboard/index.html'
    def get(self, request):
        bbs = Bb.objects.order_by('-published')
        rubrics = Rubric.objects.annotate(cnt=Count('bb')).filter(cnt__gt=0)
        context = {'bbs': bbs, 'rubrics': rubrics}
        return render(request, 'bboard/index.html', context)

# def index(request):
#
#     data = {'title': 'Мотоцикл', 'content': 'Старый', 'price': 10_000.0}
#     return JsonResponse(data)


# def index(request):
    # filename = r'c:/image/image.png'
    # return FileResponse(open(filename, 'rb'))

    # filename = r'c:/archives/archive.rar'
    # return FileResponse(open(filename, 'rb'), as_attachment=True)

# def index(request):
#     resp_content = ('Здесь будет', ' главная', ' страница', ' сайта')
#     resp = StreamingHttpResponse(resp_content, content_type='text/plain; charset=utf-8')
#
#
#     return resp

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
    # bbs = Bb.objects.filter(rubric=rubric_id)
    bbs = get_list_or_404(Bb, rubric=rubric_id)
    # rubrics = Rubric.objects.all()
    rubrics = Rubric.objects.annotate(cnt=Count('bb')).filter(cnt__gt=0)
    current_rubric = Rubric.objects.get(pk=rubric_id)

    # bbs = current_rubric.objects.all()

    context = {'bbs': bbs, 'rubrics': rubrics, 'current_rubric': current_rubric}

    return render(request, 'bboard/by_rubric.html', context)

# class BbRubricBbsView(TemplateView):
#     template_name = 'bboard/rubric_bbs.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["bbs"] = Bb.objects.filter(rubric=context['rubric_id'])
#         context["rubrics"] = Rubric.objects.annotate(cnt=Count('bb')).filter(cnt__gt=0)
#         context['current_rubric'] = Rubric.objects.get(pk=context["rubric_id"])
#         return context

class BbRubricBbsView(ListView):
    template_name = 'bboard/rubric_bbs.html'
    context_object_name = 'bbs'

    def get_queryset(self):
        return Bb.objects.filter(rubric=self.kwargs['rubric_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.annotate(cnt=Count('bb')).filter(cnt__gt=0)
        context['current_rubric'] = Rubric.objects.get(pk=self.kwargs['rubric_id'])

        return context

class BbCreateView(CreateView):
    template_name = 'bboard/bb_create.html'
    model = Bb
    form_class = BbForm
    success_url = reverse_lazy('bboard:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.annotate(cnt=Count('bb')).filter(cnt__gt=0)
        return context

# class BbCreateView(View):
#     def get(self, request, *args, **kwargs):
#         form = BbForm
#         context = {'form': form, 'rubrics': Rubric.objects.annotate(cnt=Count('bb')).filter(cnt__gt=0)}
#         return render(request, 'bboard/bb_create.html', context)
#
#     def post(self, request, *args, **kwargs):
#         form = BbForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('bboard:by_rubric', rubric_id=form.cleaned_data['rubric'].pk)
#         else:
#             context = {'form': form, 'rubrics': Rubric.objects.annotate(cnt=Count('bb')).filter(cnt__gt=0)}
#             return render(request, 'bboard/bb_create.html', context)

# class BbCreateView(FormView):
#     template_name = 'bboard/bb_create.html'
#     form_class = BbForm
#     initial = {'price': 0.0}
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['rubrics'] = Rubric.objects.annotate(cnt=Count('bb')).filter(cnt__gt=0)
#
#         return context
#
#     def form_valid(self, form):
#         form.save()
#         return super().form_valid(form)
#
#     def get_form(self, form_class=None):
#         self.object = super().get_form(form_class)
#         return self.object
#
#     def get_success_url(self):
#         return reverse('bboard:by_rubric', kwargs={'rubric_id': self.object.cleaned_data['rubric'].pk})




@require_http_methods(['GET', 'POST'])
def add_and_save(request):
    #
    # for a in request.META:
    #     with open('1.txt', 'r') as file:
    #         file.write(str(a))
    #
    # if not request.user.is_authenticated:
    #     return HttpResponseRedirect(reverse('bboard:index'))
    if request.method == 'POST':
        bbf = BbForm(request.POST)

        if bbf.is_valid():
            bbf.save()
            # return HttpResponseRedirect(reverse('bboard:by_rubric', kwargs={'rubric_id': bbf.cleaned_data['rubric'].pk}))
            return redirect('bboard:by_rubric', rubric_id=bbf.cleaned_data['rubric'].pk)
        else:
            context = {'form': bbf}
            return render(request, 'bboard/bb_create.html', context)
    else:
        bbf = BbForm()
        context = {'form': bbf}
        return render(request, 'bboard/bb_create.html', context)

def bb_detail(request, bb_id):
    try:
        # bb = Bb.objects.get(pk=bb_id)
        bb = get_object_or_404(Bb, pk=bb_id)

    except Bb.DoesNotExist:
        return Http404('Такое обьявлени не существует')

    rubrics = Rubric.objects.annotate(cnt=Count('bb')).filter(cnt__gt=0)
    context = {'bb': bb, 'rubrics': rubrics}

    return render(request, 'bboard/bb_detail.html', context)

class BbDetail(View):
    def get(self, request, bb_id):
        rubrics = Rubric.objects.annotate(cnt=Count('bb')).filter(cnt__gt=0)
        bb = get_object_or_404(Bb, pk=bb_id)
        context = {'bb': bb, 'rubrics': rubrics}
        return render(request, 'bboard/bb_detail.html', context)

class BbEditView(UpdateView):
    model = Bb
    form_class = BbForm
    success_url = reverse_lazy('bboard:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.annotate(cnt=Count('bb')).filter(cnt__gt=0)
        return context

class BbDetailView(DetailView):
    model = Bb

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.annotate(cnt=Count('bb')).filter(cnt__gt=0)

        return context

class BbDeleteView(DeleteView):
    model = Bb
    success_url = '/{rubric_id}/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.annotate(cnt=Count('bb')).filter(cnt__gt=0)

        return context