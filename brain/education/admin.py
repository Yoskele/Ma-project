from django.contrib import admin

from .models import Category, Course, Lesson, UserProgress



class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

class CourseAdmin(admin.ModelAdmin):
    list_display = ['title']

class LessonAdmin(admin.ModelAdmin):
    list_display = ['title']


class UserProgressAdmin(admin.ModelAdmin):
    list_display = ['user']

admin.site.register(Category, CategoryAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(UserProgress, UserProgressAdmin)


