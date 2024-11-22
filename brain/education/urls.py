from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    # Admin and Authentication
    path('', views.dashboard, name='dashboard'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),

    # Category Management
    path('categories/', views.category_list, name='category_list'),
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    path('category/view/<slug:slug>/', views.view_category, name='view-category'),
    path('category/delete/<int:category_id>/', views.delete_category, name='delete-category'),
    path('category/edit/<int:category_id>/', views.edit_category, name='edit-category'),

    # Course Management
    path('course/view/<slug:slug>/', views.view_course, name='view-course'),
    path('course/delete/<int:course_id>/', views.delete_course, name='delete-course'),
    path('course/edit/<int:course_id>/', views.edit_course, name='edit-course'),

    # Lesson Management
    path('lesson/<int:id>/', views.lesson_detail, name='lesson-detail'),
    path('lesson/add/', views.add_lesson, name='add-lesson'),
    path('lesson/delete/<int:lesson_id>/', views.delete_lesson, name='delete-lesson'),
    path('lesson/edit/<int:lesson_id>/', views.edit_lesson, name='edit-lesson'),
    path('lesson/search/', views.search_lesson, name='search-lesson'),

    # User Management
    path('user/create/', views.create_user, name='create_user'),
    path('user/view/<slug:slug>/', views.view_user, name='view-user'),
    path('user/delete/<int:user_id>/', views.delete_user, name='delete-user'),
    path('user/edit/<int:user_id>/', views.edit_user, name='edit-user'),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
