from django.contrib import admin

from .models import SelfIntroduction
from .models import FreeBoard
from .models import QuestionBoard
from .models import Analysis_Result

# Register your models here.
class SelfIntroductionAdmin(admin.ModelAdmin):
    list_display = ['title', 'name', 'company_name', 'registered_date']

class AnalysisResultAdmin(admin.ModelAdmin):
    list_display = ['instruction', 'plagiarism_percent', 'pass_percent', 'registered_date']

class FreeBoardAdmin(admin.ModelAdmin):
    list_display = ['title', 'name', 'registered_date']

class QuestionBoardAdmin(admin.ModelAdmin):
    list_display = ['title', 'name', 'registered_date']

admin.site.register(SelfIntroduction, SelfIntroductionAdmin)
admin.site.register(Analysis_Result, AnalysisResultAdmin)
admin.site.register(FreeBoard, FreeBoardAdmin)
admin.site.register(QuestionBoard, QuestionBoardAdmin)

