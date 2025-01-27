from bboard.models import Rubric
from django.db.models import Count

# def my_middleware(next):
#     def core_middleware(request):
#         response = next(request)
#         return response
#     return core_middleware
#
# class MyMiddleware:
#     def __init__(self, next):
#         self.next = next
#
#     def __call__(self, request):
#         response = next(request)
#         return response

# class RubricMiddleware:
#     def __init__(self, next):
#         self.next = next
#
#     def __call__(self, request):
#         return self.next(request)
#
#     def process_template_response(self, request, response):
#         response.context_data['rubric'] = Rubric.objects.all()
#         return response


def rubrics(request):
    return {'rubrics': Rubric.objects.annotate(cnt=Count('bb')).filter(cnt__gt=0)}

def process_request(request):
    if request.user.is_authenticated:
        user = request.user
        groups = user.groups.values_list('name', flat=True)
        return {'User Info': user, 'Groups': groups}
    else:
        return {'User Info': None}