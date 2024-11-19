from django import forms
from .models import Lesson, Category
from django.forms.widgets import DateTimeInput
from django_ckeditor_5.widgets import CKEditor5Widget


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Username', 
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Password'
        })
    )


class CreateLessonForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )

    class Meta:
        model = Lesson
        fields = ('slug', 'title', 'content', 'category', 'is_published')
        labels = {
            'content': 'Please write content for the lesson...',
        }
        widgets = {
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': CKEditor5Widget(attrs={"class": "django_ckeditor_5"}, config_name="extends"),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    