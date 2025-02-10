from django.db.models import Count

from bboard.models import Rubric


def my_middleware(next):
    # Какая-то инициализация
    def core_middleware(request):
        # обработка клиентского запроса
        response = next(request)
        # обработка ответа
        return response
    return core_middleware


class MyMiddleware:
    def __init__(self, next):
        self.next = next
        # Какая-то инициализация

    def __call__(self, request):
        # обработка клиентского запроса
        response = self.next(request)
        # обработка ответа
        return response


class RubricMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_template_response(self, request, response):
        print('MIDDLEWARE')
        response.context_data['rubrics'] = Rubric.objects.all()
        return response


def rubrics(request):
    # return {'rubrics': Rubric.objects.all()}
    return {'rubrics': Rubric.objects.annotate(cnt=Count('bb')).filter(cnt__gt=0)}
