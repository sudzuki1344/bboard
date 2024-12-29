from django.views.generic import ListView
from testapp.models import SMS

class SmsListView(ListView):
    model = SMS
    template_name = 'testapp/sms_list.html'
    context_object_name = 'sms_list'
    paginate_by = 10

