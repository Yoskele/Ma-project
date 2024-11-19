from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from .import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('categories/', views.category_list, name='category_list'),
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    path('lesson/<int:id>/', views.lesson_detail, name='lesson-detail'),
    path('add-lesson', views.add_lesson, name='add-lesson'),
    path('delete-lesson/<int:lesson_id>/', views.delete_lesson, name='delete-lesson'),
    path('edit-lesson-<int:lesson_id>/', views.edit_lesson, name='edit-lesson'),
    path('search-lesson/', views.search_lesson, name='search-lesson'),
]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)