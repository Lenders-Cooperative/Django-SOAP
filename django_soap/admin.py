from django.contrib import admin
from django_soap.models import *

# Register your models here.
class SOAPRequstLoggerAdmin(admin.ModelAdmin):
    ...

class SOAPResponseLoggerAdmin(admin.ModelAdmin):
    ...

admin.site.register(SOAPResponseLogger, SOAPResponseLoggerAdmin)
admin.site.register(SOAPRequestLogger, SOAPRequstLoggerAdmin)