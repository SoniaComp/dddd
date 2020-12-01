from django.contrib import admin
from core.models import *
# Register your models here.

admin.site.register(Tag)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Event)
admin.site.register(EventComp)
admin.site.register(AIAnswer)
admin.site.register(PanryeData)