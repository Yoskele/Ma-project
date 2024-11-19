from django.contrib import admin

from .models import Lesson, Category



class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

class LessonAdmin(admin.ModelAdmin):
    list_display = ['title']




admin.site.register(Category, CategoryAdmin)
admin.site.register(Lesson, LessonAdmin)



