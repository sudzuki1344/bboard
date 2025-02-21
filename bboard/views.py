from django.contrib.auth import get_user, authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.core.paginator import Paginator
from django.db import transaction, DatabaseError
from django.db.models import Count
from django.forms import modelformset_factory
from django.forms.models import inlineformset_factory
from django.http import (HttpResponse, HttpResponseRedirect, HttpResponseNotFound,
                         Http404, StreamingHttpResponse, FileResponse, JsonResponse)
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.template import loader
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.views.decorators.cache import cache_page
from django.views.decorators.http import (require_http_methods,
                                          require_GET, require_POST, require_safe)
from django.views.decorators.vary import vary_on_headers, vary_on_cookie
from django.views.generic.base import RedirectView
from django.views.generic.dates import ArchiveIndexView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView, SingleObjectMixin
from django.views.generic.base import View, TemplateView
from django.views.generic.edit import CreateView, FormView, UpdateView, DeleteView
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from bboard.forms import BbForm, RubricBaseFormSet, SearchForm
from bboard.models import Bb, Rubric, Img
from bboard.serializers import RubricSerializer, BbSerializer
from bboard.signals import add_bb
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

# Основной (вернуть)
# def index(request):
#     bbs = Bb.objects.order_by('-published')
#     # rubrics = Rubric.objects.all()
#     rubrics = Rubric.objects.annotate(cnt=Count('bb')).filter(cnt__gt=0)
#     context = {'bbs': bbs, 'rubrics': rubrics}
#
#     return render(request, 'bboard/index.html', context)


# @cache_page(60 * 5)
# @cache_page(30)
# @vary_on_headers('User-Agent')
# @vary_on_headers('Cookie')
# @vary_on_headers('User-Agent', 'Cookie')
# @vary_on_cookie
def index(request):
    bbs = Bb.objects.order_by('-published')
    # rubrics = Rubric.objects.annotate(cnt=Count('bb')).filter(cnt__gt=0)

    paginator = Paginator(bbs, 2)

    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1

    page = paginator.get_page(page_num)

    # context = {'bbs': page.object_list, 'rubrics': rubrics, 'page': page}


    # if 'counter' in request.COOKIES:
    #     cnt = int(request.COOKIES['counter']) + 1
    # else:
    #     cnt = 1
    #
    # context = {'bbs': page.object_list, 'page': page, 'counter': cnt}
    #
    # response = render(request, 'bboard/index.html', context)
    # response.set_cookie('counter', cnt)
    # return response

    if 'counter' in request.session:
        cnt = request.session['counter'] + 1
    else:
        cnt = 1

    request.session['counter'] = cnt

    context = {'bbs': page.object_list, 'page': page, 'counter': cnt}

    return render(request, 'bboard/index.html', context)


class BbIndexView(ArchiveIndexView):
    model = Bb
    date_field = 'published'
    date_list_period = 'year'
    template_name = 'bboard/index.html'
    context_object_name = 'bbs'
    allow_empty = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.annotate(
                                            cnt=Count('bb')).filter(cnt__gt=0)
        return context


class BbRedirectView(RedirectView):
    url = '/'


def by_rubric(request, rubric_id):
    # bbs = Bb.objects.filter(rubric=rubric_id)
    bbs = get_list_or_404(Bb, rubric=rubric_id)
    # rubrics = Rubric.objects.all()
    # rubrics = Rubric.objects.annotate(cnt=Count('bb')).filter(cnt__gt=0)
    current_rubric = Rubric.objects.get(pk=rubric_id)

    # bbs = current_rubric.entries.all()

    # context = {'bbs': bbs, 'rubrics': rubrics, 'current_rubric': current_rubric}
    context = {'bbs': bbs, 'current_rubric': current_rubric}

    return render(request, 'bboard/by_rubric.html', context)


# Основной, вернуть
class BbRubricBbsView(ListView):
    template_name = 'bboard/rubric_bbs.html'
    context_object_name = 'bbs'

    def get_queryset(self):
        return Bb.objects.filter(rubric=self.kwargs['rubric_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['rubrics'] = Rubric.objects.annotate(
        #                                     cnt=Count('bb')).filter(cnt__gt=0)
        context['current_rubric'] = Rubric.objects.get(
                                                   pk=self.kwargs['rubric_id'])
        return context


# class BbRubricBbsView(SingleObjectMixin, ListView):
#     template_name = 'bboard/rubric_bbs.html'
#     pk_url_kwarg = 'rubric_id'
#
#     def get(self, request, *args, **kwargs):
#         self.object = self.get_object(queryset=Rubric)
#         return super().get(request, *args, **kwargs)
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['current_rubric'] = self.object
#         context['rubrics'] = Rubric.objects.all()
#         context['bbs'] = context['object_list']
#         return context
#
#     def get_queryset(self):
#         return self.object.bb_set.all()


# Основной (вернуть)
class BbCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    template_name = 'bboard/bb_create.html'
    model = Bb
    form_class = BbForm
    success_url = reverse_lazy('bboard:index')
    # initial = {'price': 1000.0}

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        response = super().form_valid(form)
        add_bb.send(sender=self.__class__, instance=self.object)
        return response

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['rubrics'] = Rubric.objects.annotate(
    #                                         cnt=Count('bb')).filter(cnt__gt=0)
    #     return context


def add_and_save(request):
    if request.method == 'POST':
        bbf = BbForm(request.POST)

        # bbf = BbForm(request.POST, request.FILES)

        # bbf = BbForm(request.POST, request.FILES)
        # if bbf.is_valid():
        #     for file in request.FILES.getlist('img'):
        #         img = Img()
        #         img.desc = bbf.cleaned_data['desc']
        #         img.img = file
        #         img.save()

        if bbf.is_valid():
            bbf.save()
            # return HttpResponseRedirect(reverse('bboard:by_rubric',
            #             kwargs={'rubric_id': bbf.cleaned_data['rubric'].pk}))
            return redirect('bboard:by_rubric',
                            rubric_id=bbf.cleaned_data['rubric'].pk)
        else:
            context = {'form': bbf}
            return render(request, 'bboard/bb_create.html', context)
    else:
        # bbf = BbForm(initial={'price': 1000.0})
        bbf = BbForm()
        context = {'form': bbf}
        return render(request, 'bboard/bb_create.html', context)


# Основной, вернуть
class BbEditView(UpdateView):
    model = Bb
    form_class = BbForm
    success_url = reverse_lazy('bboard:index')
    success_message = 'Объявление успешно исправлено!'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['rubrics'] = Rubric.objects.annotate(
    #                                         cnt=Count('bb')).filter(cnt__gt=0)
    #     return context


def edit(request, pk):
    bb = Bb.objects.get(pk=pk)
    if request.method == 'POST':
        bbf = BbForm(request.POST, instance=bb)
        if bbf.is_valid():
            # if bbf.has_changed():
            bbf.save()
            return HttpResponseRedirect(reverse('bboard:by_rubric',
                        kwargs={'rubric_id': bbf.cleaned_data['rubric'].pk}))
        else:
            context = {'form': bbf}
            return render(request, 'bboard/bb_form.html', context)
    else:
        bbf = BbForm(instance=bb)
        context = {'form': bbf}
        return render(request, 'bboard/bb_form.html', context)


def bb_detail(request, bb_id):
    try:
        # bb = Bb.objects.get(pk=bb_id)
        bb = get_object_or_404(Bb, pk=bb_id)
    except Bb.DoesNotExist:
        # return HttpResponseNotFound('Такое объявление не существует')
        return Http404('Такое объявление не существует')

    rubrics = Rubric.objects.annotate(cnt=Count('bb')).filter(cnt__gt=0)
    context = {'bb': bb, 'rubrics': rubrics}

    return render(request, 'bboard/bb_detail.html', context)


class BbDetailView(DetailView):
    model = Bb

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['rubrics'] = Rubric.objects.annotate(
    #                                         cnt=Count('bb')).filter(cnt__gt=0)
    #     return context


class BbDeleteView(DeleteView):
    model = Bb
    success_url = '/{rubric_id}/'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['rubrics'] = Rubric.objects.annotate(
    #                                         cnt=Count('bb')).filter(cnt__gt=0)
    #     return context


@login_required(login_url='/login/')
@user_passes_test(lambda user: user.is_staff)
# @permission_required('bboard.add_rubric')
def rubrics(request):
    RubricFormSet = modelformset_factory(Rubric, fields=('name',),
                                         can_order=True,
                                         can_delete=True,
                                         formset=RubricBaseFormSet,
                                         # extra=3
                                         )

    if request.method == 'POST':
        formset = RubricFormSet(request.POST)
        if formset.is_valid():
            formset.save(commit=False)
            for form in formset:
                if form.cleaned_data:
                    rubric = form.save(commit=False)
                    if rubric in formset.deleted_objects:
                        rubric.delete()
                    else:
                        if form['ORDER'].data:
                            rubric.order = form['ORDER'].data
                        rubric.save()
            return redirect('bboard:index')
    else:
        formset = RubricFormSet()
    context = {'formset': formset}
    return render(request, 'bboard/rubrics.html', context)


def bbs(request, rubric_id):
    BbsFormSet = inlineformset_factory(Rubric, Bb,
                                       form=BbForm, extra=1)
    rubric = Rubric.objects.get(pk=rubric_id)
    if request.method == 'POST':
        formset = BbsFormSet(request.POST, instance=rubric)
        if formset.is_valid():
            formset.save()
            return redirect('bboard:index')
    else:
        formset = BbsFormSet(instance=rubric)
    context = {'formset': formset, 'current_rubric': rubric}
    return render(request, 'bboard/bbs.html', context)


def commit_handler():
    pass
    # Действия после подтверждения транзакции


# @transaction.non_atomic_requests  # не атомарные  'ATOMIC_REQUEST': False,
# @transaction.atomic               # атомарные     'ATOMIC_REQUEST': True,
def my_view(request):
    # if formset.is_valid():
    #     with transaction.atomic():
    #         for form in formset:
    #             if form.cleaned_data:
    #                 with transaction.atomic():
    #                     pass

    # try:
    #     with transaction.atomic():
    #         # сохранить данные в БД
    #         pass
    # except DatabaseError:
    #     # Реагируем на ошибки
    #     pass

    # bbs = Bb.objects.select_for_updates().filter(price__lt=100)
    bbs = Bb.objects.select_for_updates(skip_locked=True,
                                        of=('self', 'rubric')).filter(price__lt=100)
    # with transaction.atomic():
    #     for bb in bbs:
    #         bb.price = 100
    #         bb.save()

    # if form.is_valid():
    #     try:
    #         form.save()
    #         transaction.commit()
    #     except:
    #         transaction.rollback()

    # if formset.is_valid():
    #     for form in formset:
    #         if form.cleaned_data:
    #             sp = transaction.savepoint()
    #             try:
    #                 form.save()
    #                 transaction.savepoint_commit(sp)
    #             except:
    #                 transaction.savepoint_rollback(sp)
    #             transaction.commit()

    #             transaction.on_commit(commit_handler)

    return redirect('bboard:index')


def search(request):
    if request.method == 'POST':
        sf = SearchForm(request.POST)
        if sf.is_valid():
            keyword = sf.cleaned_data['keyword']
            rubric_id = sf.cleaned_data['rubric'].pk
            # bbs = Bb.objects.filter(title__icontains=keyword,
            #                         rubric=rubric_id)

            bbs = Bb.objects.filter(title__iregex=keyword,
                                    rubric=rubric_id)

            messages.add_message(request, messages.SUCCESS,
                                 'Слово найдено!', extra_tags='first second')

            # messages.success(request, 'Слово найдено!')

            context = {'bbs': bbs, 'form': sf}
            return render(request, 'bboard/search_results.html', context)
    else:
        sf = SearchForm()

    context = {'form': sf}
    return render(request, 'bboard/search.html', context)


def delete_img(request, pk):
    img = Img.objects.get(pk=pk)
    img.img.delete(save=False)
    img.delete()
    return redirect('bboard:index')


def my_login(request):
    user_name = request.POST['username']
    pass_word = request.POST['password']
    user = authenticate(request, username=user_name, password=pass_word)

    if user is not None:
        login(request, user)
        return render(request, 'bboard/login.html',
                      {'user': user})

    return redirect('bboard:index')

def my_logout(request):
    logout(request)
    return redirect('bboard:index')


###########
### DRF ###
###########
@api_view(['GET', 'POST'])
# @permission_classes((IsAuthenticated,))
def api_rubrics(request):
    if request.method == 'GET':
        rubrics = Rubric.objects.all()
        serializer = RubricSerializer(rubrics, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = RubricSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def api_rubric_detail(request, pk):
    rubric = Rubric.objects.get(pk=pk)

    if request.method == 'GET':
        serializer = RubricSerializer(rubric)
        return Response(serializer.data)

    elif request.method == 'PUT' or request.method == 'PATCH':
        serializer = RubricSerializer(rubric, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        rubric.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# class APIRubrics(APIView):
#     def get(self, request):
#         rubrics = Rubric.objects.all()
#         serializer = RubricSerializer(rubrics, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = RubricSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,
#                             status=status.HTTP_201_CREATED)
#         return Response(serializer.errors,
#                         status=status.HTTP_400_BAD_REQUEST)


class APIRubrics(generics.ListCreateAPIView):
    queryset = Rubric.objects.all()
    serializer_class = RubricSerializer


class APIRubricDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Rubric.objects.all()
    serializer_class = RubricSerializer

class APIRubricList(generics.ListAPIView):
    queryset = Rubric.objects.all()
    serializer_class = RubricSerializer

class APIRubricViewSet(ModelViewSet):
    queryset = Rubric.objects.all()
    serializer_class = RubricSerializer
    # permission_classes = (IsAuthenticated,)
    
    def get_queryset(self):
        queryset = Rubric.objects.all()
        name = self.request.query_params.get('name', None)
        if name is not None:
            queryset = queryset.filter(name__icontains=name)
        return queryset
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            response_data = {
                'count': self.paginator.page.paginator.count,
                'results': serializer.data,
                'metadata': {
                    'total_rubrics': Rubric.objects.count(),
                    'has_bbs': queryset.filter(bb__isnull=False).exists()
                }
            }
            return self.get_paginated_response(response_data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        response_data = {
            'data': serializer.data,
            'message': 'Rubric created successfully',
            'status': 'success'
        }
        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        response_data = {
            'data': serializer.data,
            'message': 'Rubric updated successfully',
            'status': 'success',
            'related_bbs_count': instance.bb_set.count()
        }
        return Response(response_data)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        bbs_count = instance.bb_set.count()
        if bbs_count > 0:
            return Response({
                'message': f'Cannot delete rubric with {bbs_count} associated bulletin boards',
                'status': 'error'
            }, status=status.HTTP_400_BAD_REQUEST)
        self.perform_destroy(instance)
        return Response({
            'message': 'Rubric deleted successfully',
            'status': 'success'
        }, status=status.HTTP_204_NO_CONTENT)

class ApiBbViewSet(ModelViewSet):
    queryset = Bb.objects.all()
    serializer_class = BbSerializer