from django.db import models
from django.conf import settings
from django.utils import timezone


# Create your models here.

# 자유게시판
class Post(models.Model):
    objects = models.Manager()
    name = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, verbose_name='작성자', on_delete=models.CASCADE)
    title = models.CharField(max_length=120, verbose_name="제목")
    contents = models.TextField(verbose_name="내용", null=True)
    registered_date = models.DateTimeField(auto_now_add=True, null=True, verbose_name="등록시간")
    #published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

class Self_introduction(models.Model):
    objects = models.Manager()

    title = models.CharField(max_length=120, verbose_name="제목", null=True)
    name = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, verbose_name='작성자', on_delete=models.CASCADE)

    # 추후 동적으로 결과 생성하기
    #questions = []
    #answers = []
    #password = models.CharField(max_length=120, default = '', null=True)

    question_1 = models.CharField(max_length=120, default='', null=True)
    question_2 = models.CharField(max_length=120, default='', null=True)
    question_3 = models.CharField(max_length=120, default='', null=True)
    question_4 = models.CharField(max_length=120, default='', null=True)
    question_5 = models.CharField(max_length=120, default='', null=True)

    answer_1 = models.TextField(default='', null=True)
    answer_2 = models.TextField(default='', null=True)
    answer_3 = models.TextField(default='', null=True)
    answer_4 = models.TextField(default='', null=True)
    answer_5 = models.TextField(default='', null=True)

    registered_date = models.DateTimeField(auto_now_add=True, verbose_name="등록시간", null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

class Plagiarism_result(models.Model):
    objects = models.Manager()

    title = models.CharField(max_length=120, verbose_name="제목", null=True)
    name = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, verbose_name='작성자', on_delete=models.CASCADE)
    id_value = models.IntegerField(default=0)
    registered_date = models.DateTimeField(auto_now_add=True, verbose_name="등록시간", null=True)
    
    ###################################################################################################################
    plagiarism_result1 = models.TextField(default='', null=True)
    plagiarism_result2 = models.TextField(default='', null=True)
    plagiarism_result3 = models.TextField(default='', null=True)
    plagiarism_result4 = models.TextField(default='', null=True)
    plagiarism_result5 = models.TextField(default='', null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

class Grammar_result(models.Model):
    objects = models.Manager()

    title = models.CharField(max_length=120, verbose_name="제목", null=True)
    name = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, verbose_name='작성자', on_delete=models.CASCADE)
    id_value = models.IntegerField(default=0)
    registered_date = models.DateTimeField(auto_now_add=True, verbose_name="등록시간", null=True)

    ###################################################################################################################
    grammar_result1 = models.TextField(default='', null=True)
    grammar_result2 = models.TextField(default='', null=True)
    grammar_result3 = models.TextField(default='', null=True)
    grammar_result4 = models.TextField(default='', null=True)
    grammar_result5 = models.TextField(default='', null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

class Pass_result(models.Model):
    objects = models.Manager()

    title = models.CharField(max_length=120, verbose_name="제목", null=True)
    name = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, verbose_name='작성자', on_delete=models.CASCADE)
    id_value = models.IntegerField(default=0)
    registered_date = models.DateTimeField(auto_now_add=True, verbose_name="등록시간", null=True)

    ###################################################################################################################
    pass_result1 = models.TextField(default='', null=True)
    pass_result2 = models.TextField(default='', null=True)
    pass_result3 = models.TextField(default='', null=True)
    pass_result4 = models.TextField(default='', null=True)
    pass_result5 = models.TextField(default='', null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title