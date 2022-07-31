from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Category)
admin.site.register(Policy)
admin.site.register(PolicyRecord)
admin.site.register(Question)
admin.site.register(Contact)
