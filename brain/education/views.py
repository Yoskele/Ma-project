from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import LoginForm, CreateUserForm, CreateLessonForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Category, Course, Lesson, UserProfile


@login_required
def create_user(request):
    if not request.user.is_superuser:  # Ensure only superusers can access this view
        messages.error(request, "You do not have permission to create users.")
        return redirect("dashboard")
    print('if not.')
    if request.method == "POST":
        form = CreateUserForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()  # Save the user
            UserProfile.objects.create(user=user)  # Create the UserProfile automatically
            messages.success(request, f"User {user.username} created successfully!")
            return redirect("dashboard")  # Redirect to the dashboard or another page
    else:
        form = CreateUserForm()

    return render(request, "components/user/create-user.html", {"form": form})


@login_required
def view_user(request, slug):
    return render(request, "components/user/view-user.html")

@login_required
def delete_user(request):
    return render(request, "components/user/create-user.html", {"form": form})


@login_required
def edit_user(request):
    return render(request, "components/user/edit-user.html", {"form": form})

@login_required
def edit_category(request):
    return render(request, "components/create-category.html", {"form": form})


@login_required
def view_category(request):
    return render(request, "components/view-category.html", {"form": form})

@login_required
def delete_category(request):
    return render(request, "components/create-category.html", {"form": form})

@login_required
def edit_category(request):
    return render(request, "components/create-category.html", {"form": form})



@login_required
def view_course(request):
    return render(request, "components/view-course.html", {"form": form})

@login_required
def delete_course(request):
    return render(request, "components/create-course.html", {"form": form})

@login_required
def edit_course(request):
    return render(request, "components/create-course.html", {"form": form})


















from bs4 import BeautifulSoup

def generate_toc(lesson_content):
    soup = BeautifulSoup(lesson_content, 'html.parser')
    toc = []

    # Extract headings (h1, h2, h3, etc.)
    for heading in soup.find_all(['h1', 'h2', 'h3']):
        toc.append({
            'level': heading.name,  # e.g., 'h1', 'h2'
            'text': heading.text.strip(),
            'id': heading.get('id') or heading.text.strip().replace(' ', '-').lower()
        })
        # Add IDs to headings if they do not already have one
        heading['id'] = toc[-1]['id']

    # Return the modified content and TOC
    return str(soup), toc








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
    updated_content, toc = generate_toc(lesson.content)  # Use the function above
    lesson.content = updated_content  # Update the content to include IDs
    return render(request, 'components/lesson_detail.html', {'lesson': lesson, 'toc': toc})

@login_required
def dashboard(request):
    try:
        categories = Category.objects.all().order_by('-created_at')
        courses = Course.objects.all().order_by('-created_at')
        lessons = Lesson.objects.all().order_by('-created_at')
        users = None
        if request.user.is_superuser:
            users = UserProfile.objects.all().order_by('user')
    except Exception as e:
        print('Exception: ', e)
    context = {
        'categories': categories,
        'courses': courses,
        'lessons': lessons,
        'users': users,
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


