from django.contrib.admin.templatetags.admin_list import pagination
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Book, Comment, UserLibrary
from django.contrib.auth import login
from .forms import ContactForm, BookForm, FeedbackForm, RegistrationForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
# Create your views here.

@login_required
def home(request):
    user_library = UserLibrary.objects.filter(user=request.user)
    books = [entry.book for entry in user_library]
    context = {
        'title': 'Home Page',
        'message': 'Welcome to the Home Page!',
        'books': books,
    }
    return render(request, 'pages/home.html', context)


def about(request):
    context = {
        'title': 'About us',
        'message': 'We are a team that creates more than just a website.',
    }
    return render(request, 'pages/about.html', context)


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            return HttpResponse("Thank you for your message!")
    else:
        form = ContactForm()

    context = {
        'form': form,
        'title': 'Contact Us',
        'message': 'Welcome to the Contact Page!'
    }
    return render(request, 'pages/contact.html', context)


def create(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.save()
            return redirect('blog')
    else:
         form = BookForm()
    context = {
        'title': 'Create book',
        'message': 'Welcome to the Create Book Page!',
        'form': form
    }
    return render(request, 'pages/create.html', context)

@login_required
def blog(request):
    from django.core.paginator import Paginator
    books = Book.objects.all().order_by('-publish_date')
    paginator = Paginator(books, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'pages/blog.html', {'page_obj': page_obj, 'title': 'Blog'})

def feedback_view(request):
    success = False
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            success = True
            form = FeedbackForm()
    else:
        form = FeedbackForm()

    return render(request, 'pages/feedback.html', {'form': form, 'success': success})


def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('home')
    form = RegistrationForm()
    context = {
        'title': 'Register Page',
        'message': 'Welcome to the register Page!',
        'form' : form
    }
    return render(request, 'pages/register.html', context)


@login_required
def book_detail_view(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    user = request.user
    already_added = UserLibrary.objects.filter(user=user, book=book).exists()

    if request.method == "POST":

        if 'remove_from_library' in request.POST:
            UserLibrary.objects.filter(user=user, book=book).delete()
            return redirect('book_detail', book_id=book.id)

        if 'add_to_library' in request.POST:
            UserLibrary.objects.get_or_create(user=user, book=book)
            return redirect('book_detail', book_id=book.id)

        if 'comment_submit' in request.POST:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.user = user
                comment.book = book
                comment.save()
                return redirect('book_detail', book_id=book.id)
        else:
            form = CommentForm()
    else:
        form = CommentForm()

    comments = book.comments.all().order_by('-created_at')

    context = {
        'book': book,
        'already_added': already_added,
        'comments': comments,
        'form': form,
    }
    return render(request, 'pages/book_detail.html', context)




@login_required
def search(request):
    query = request.GET.get('q', '')
    results = []
    if query:
        results = Book.objects.filter(title__icontains=query)
    return render(request, 'pages/search_results.html', {'results': results, 'query': query})


@login_required
def remove_from_library(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    user_library_entry = UserLibrary.objects.filter(user=request.user, book=book).first()

    if user_library_entry:
        user_library_entry.delete()
        messages.success(request, f"Book «{book.title}» removed from your library.")
    else:
        messages.warning(request, "This book was not in your library..")

    return redirect('home')