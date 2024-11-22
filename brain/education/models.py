from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django_ckeditor_5.fields import CKEditor5Field


# Category Model
class Category(models.Model):
    slug = models.SlugField(max_length=120, unique=True)
    name = models.CharField(max_length=120, unique=True)
    meta_title = models.CharField(max_length=500, blank=True)
    meta_description = models.TextField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name).lower()
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


# Course Model
class Course(models.Model):
    slug = models.SlugField(max_length=255, unique=True)
    title = models.CharField(max_length=255)
    description = CKEditor5Field('Description', config_name='default')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="courses")
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title).lower()
        super(Course, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


# Lesson Model
class Lesson(models.Model):
    slug = models.SlugField(max_length=255, unique=True)
    title = models.CharField(max_length=255)
    content = CKEditor5Field('Content', config_name='default')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons")
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title).lower()
        super(Lesson, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


# User Progress Model
class UserProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="user_progress")
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="user_progress")
    is_completed = models.BooleanField(default=False)
    completed_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'lesson')

    def __str__(self):
        return f"{self.user.username} - {self.lesson.title}"

# User Profile Model
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to="profile_pictures/", blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"