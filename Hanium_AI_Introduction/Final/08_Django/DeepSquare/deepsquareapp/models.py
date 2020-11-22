from django.db import models
from django.conf import settings
from django.utils import timezone

# Create your models here.

class SelfIntroduction(models.Model):
    PASS_HOLD_FAIL_CHOICES = (
        ('PASS', 'PASS'),
        ('HOLD', 'HOLD'),
        ('FAIL', 'FAIL')
    )
    title = models.CharField(max_length=120, null=False, verbose_name="제목")
    name = models.ForeignKey(settings.AUTH_USER_MODEL, null=False, on_delete=models.CASCADE, verbose_name="작성자")
    contents = models.TextField(verbose_name="자소서 내용", null=False)

    company_name = models.CharField(max_length=120, null=False, verbose_name="회사명")
    department_name = models.CharField(max_length=120, null=True, blank=True, verbose_name="직무분야명")
    pass_fail_result = models.CharField(max_length=5, null=False, choices=PASS_HOLD_FAIL_CHOICES, default='HOLD')

    registered_date = models.DateTimeField(auto_now_add=True, null=False, verbose_name="작성일")
    #company_id = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name="회사 ID")
    #department_id = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name="직무분야 ID")

class Analysis_Result(models.Model):
    instruction = models.ForeignKey(SelfIntroduction, null=False, on_delete=models.CASCADE, verbose_name="자소서 아이디")
    plagiarism_percent = models.FloatField(max_length=100, null=False, verbose_name="표절 확률")
    pass_percent = models.FloatField(max_length=100, null=False, verbose_name="합격 확률")
    grammar_contents = models.TextField(verbose_name="맞춤법 수정본", null=True)
    correction_contents = models.TextField(verbose_name="첨삭", null=True)
    registered_date = models.DateTimeField(auto_now_add=True, null=False, verbose_name="등록시간")

class FreeBoard(models.Model):
    name = models.ForeignKey(settings.AUTH_USER_MODEL, null=False, on_delete=models.CASCADE, verbose_name="작성자")
    title = models.CharField(max_length=120, null=False, verbose_name="제목")
    contents = models.TextField(verbose_name="내용", null=False)
    registered_date = models.DateTimeField(auto_now_add=True, null=False, verbose_name="작성일")
    hits = models.PositiveIntegerField(null=False, default = 0)

    @property
    def increase_hits(self):
        self.hits += 1
        self.save()

class QuestionBoard(models.Model):
    name = models.ForeignKey(settings.AUTH_USER_MODEL, null=False, on_delete=models.CASCADE, verbose_name="작성자")
    title = models.CharField(max_length=120, null=False, verbose_name="제목")
    contents = models.TextField(verbose_name="내용", null=False)
    registered_date = models.DateTimeField(auto_now_add=True, null=False, verbose_name="작성일")
    hits = models.PositiveIntegerField(null=False, default = 0)

    @property
    def increase_hits(self):
        self.hits += 1
        self.save()

class ReviewBoard(models.Model):
    name = models.ForeignKey(settings.AUTH_USER_MODEL, null=False, on_delete=models.CASCADE, verbose_name="작성자")
    title = models.CharField(max_length=120, null=False, verbose_name="제목")
    contents = models.TextField(verbose_name="내용", null=False)
    registered_date = models.DateTimeField(auto_now_add=True, null=False, verbose_name="작성일")
    hits = models.PositiveIntegerField(null=False, default = 0)

    @property
    def increase_hits(self):
        self.hits += 1
        self.save()

class Corporate(models.Model):
    corporate_name = models.CharField(max_length=120, null=False, primary_key=True, verbose_name="회사명")
    corporate_vision = models.TextField(null=True, verbose_name="기업 비전")

class Corporate_Keyword(models.Model):
    corporate_name = models.ForeignKey(Corporate, null=False, on_delete=models.CASCADE, verbose_name="회사명")
    corporate_keyword = models.CharField(max_length=30, null=True, verbose_name="기업 키워드")

class Duties(models.Model):
    duties_name = models.CharField(max_length=120, null=False, verbose_name="직무명")
    duties_feature = models.TextField(null=True, verbose_name="직무 특성")

class Competency(models.Model):
    competency_name = models.CharField(max_length=30, null=False, verbose_name="역량명")
    competency_define = models.TextField(null=False, verbose_name="역량 정의")
