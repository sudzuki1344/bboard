from django.contrib import admin

from testapp.models import Machine

def machine_str(self):
    return self.name

Machine.__str__ = machine_str


admin.site.register(Machine)
