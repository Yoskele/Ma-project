from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import LoginForm, CreateLessonForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Category, Lesson

@login_required
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'components/category_list.html', {'categories': categories})

# from .models import Category
@login_required
def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    lessons = category.lessons.filter(is_published=True)
    return render(request, 'components/category_detail.html', {'category': category, 'lessons': lessons})

@login_required
def lesson_detail(request, id):
    lesson = get_object_or_404(Lesson, id=id, is_published=True)
    return render(request, 'components/lesson_detail.html', {'lesson': lesson})

@login_required
def dashboard(request):
    try:
        lessons = Lesson.objects.all().order_by('-created_at')
        print('lessons: ', lessons)
    except Exception as e:
        print('Exception: ', e)
    context = {
        'lessons': lessons,
    }
    return render(request, 'home-page.html', context)


@login_required
def add_lesson(request):
    if request.method == 'POST':
        form = CreateLessonForm(request.POST)
        if form.is_valid():
            form.save() 
            messages.success(request, 'Lesson saved successfully.')
            return redirect('dashboard')
    else:
        form = CreateLessonForm()
    return render(request, 'components/add_article.html', {'form': form})


@login_required
def delete_lesson(request, lesson_id):
    try:
        lesson = Lesson.objects.get(pk=lesson_id)
        lesson.delete()
        messages.success(request, 'Lesson is Deleted successful')
        return redirect('dashboard')
    except Exception as e:
        print('Exception: ', e)
    

@login_required
def edit_lesson(request, lesson_id):
    # Fetch the lesson object
    lesson = get_object_or_404(Lesson, pk=lesson_id)

    if request.method == 'POST':
        # Pass the lesson instance to the form for editing
        form = CreateLessonForm(request.POST, request.FILES, instance=lesson)
        if form.is_valid():
            form.save()
            messages.success(request, 'Edits have been saved successfully.')
            return redirect('dashboard')
    else:
        # Provide the existing lesson instance to pre-fill the form
        form = CreateLessonForm(instance=lesson)

    context = {
        'lesson': lesson,
        'form': form,
    }
    return render(request, 'components/edit-article.html', context)







from django.db.models import Q


def search_lesson(request):
    query = request.POST.get('query', '')  # Use POST since hx-post is used
    print('query: ', query)
    if query:
        results = Lesson.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )
    else:
        results = Lesson.objects.none()

    if request.htmx:  # Check if it is an HTMX request
        return render(request, 'partials/search_results.html', {'results': results})
    
    # Optional fallback for non-HTMX requests
    return render(request, 'partials/search_results.html', {'results': results})







def login_user(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('dashboard')
    else:
        form = LoginForm()
    return render(request, 'components/login-page.html', {'form': form})


# logout page
def logout_user(request):
    logout(request)
    return redirect('login')


