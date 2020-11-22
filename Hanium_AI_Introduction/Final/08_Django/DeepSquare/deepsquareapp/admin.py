from django.contrib import admin

from .models import SelfIntroduction
from .models import FreeBoard
from .models import QuestionBoard
from .models import ReviewBoard
from .models import Analysis_Result
from .models import Corporate
from .models import Corporate_Keyword
from .models import Duties
from .models import Competency


# Register your models here.
class SelfIntroductionAdmin(admin.ModelAdmin):
    list_display = ['id', 'pass_fail_result', 'title', 'name', 'company_name', 'registered_date']

class AnalysisResultAdmin(admin.ModelAdmin):
    list_display = ['instruction', 'plagiarism_percent', 'pass_percent', 'registered_date']

class FreeBoardAdmin(admin.ModelAdmin):
    list_display = ['title', 'name', 'registered_date']

class QuestionBoardAdmin(admin.ModelAdmin):
    list_display = ['title', 'name', 'registered_date']

class ReviewBoardAdmin(admin.ModelAdmin):
    list_display = ['title', 'name', 'registered_date']

class CorporateAdmin(admin.ModelAdmin):
    list_display = ['corporate_name', 'corporate_vision']

class CorporateKeywordAdmin(admin.ModelAdmin):
    list_display = ['id', 'corporate_name', 'corporate_keyword']

class DutiesAdmin(admin.ModelAdmin):
    list_display = ['id', 'duties_name', 'duties_feature']

class CompetencyAdmin(admin.ModelAdmin):
    list_display = ['id', 'competency_name', 'competency_define']

admin.site.register(SelfIntroduction, SelfIntroductionAdmin)
admin.site.register(Analysis_Result, AnalysisResultAdmin)
admin.site.register(FreeBoard, FreeBoardAdmin)
admin.site.register(QuestionBoard, QuestionBoardAdmin)
admin.site.register(ReviewBoard, ReviewBoardAdmin)
admin.site.register(Corporate, CorporateAdmin)
admin.site.register(Corporate_Keyword, CorporateKeywordAdmin)
admin.site.register(Duties, DutiesAdmin)
admin.site.register(Competency, CompetencyAdmin)