from django.contrib import admin
from .models import Post, Self_introduction, Plagiarism_result, Grammar_result, Pass_result


# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'name', 'registered_date')

class IntroAdmin(admin.ModelAdmin):
    list_display = ('title', 'name', 'registered_date')

class Plagiarism_resultAdmin(admin.ModelAdmin):
    list_display = ('title', 'name', 'registered_date')

class Grammar_resultAdmin(admin.ModelAdmin):
    list_display = ('title', 'name', 'registered_date')

class Pass_resultAdmin(admin.ModelAdmin):
    list_display = ('title', 'name', 'registered_date')

admin.site.register(Post, PostAdmin)
admin.site.register(Self_introduction, IntroAdmin)
admin.site.register(Plagiarism_result, Plagiarism_resultAdmin)
admin.site.register(Grammar_result, Grammar_resultAdmin)
admin.site.register(Pass_result, Pass_resultAdmin)