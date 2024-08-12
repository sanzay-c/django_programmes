from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Book

# Create your views here.
@login_required(login_url='/')
def add_book(request):
    if request.method == "POST":
        
        title = request.POST.get('title')
        author = request.POST.get('author')
        published_date = request.POST.get('published_date')
        price = request.POST.get('price')

        Book.objects.create(
            title = title,
            author = author,
            published_date = published_date,
            price = price,
        )

        return redirect('/add_books/')
    book = Book.objects.all()
    return render(request, 'add_book.html', context={'book': book, 'page': 'add book'})


def delete_book(request, id):
    # book = Book.objects.get(id = id)
    book =  get_object_or_404(Book, id=id)
    book.delete()

    messages.success(request, 'Book deleted successfully')
    return redirect("/add_books/")


def update_book(request, id):
    # queryset = Book.objects.get(id = id)
    book = get_object_or_404(Book, id=id) 

    if request.method == "POST":
        data = request.POST

        title = data.get('title')
        author = data.get('author')
        # published_date = data.get('published_date')
        price = data.get('price')
        
        book.title = title
        book.author = author
        # book.published_date = published_date
        book.price = price

        book.save()
        return redirect('/add_books/')

    return render(request, 'update_book.html', context = {'book' : book})


def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Logged in successfully!')
            return redirect('/add_books/')  # Redirect to a protected page
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('/')  # Redirect back to the login page
    
    return render(request, 'login.html')


def register(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        password = request.POST.get("password")

        # user = User.objects.filter(username = username)
        # if user.exists():
        #     messages.info(request, 'Username already taken')
        #     return redirect('/regsiter/')
        
        if User.objects.filter(username=username).exists():
            messages.info(request, 'Username already taken')
            return redirect('/register/')

        user = User.objects.create(
            first_name = first_name,
            last_name = last_name,
            username = username,
            password = password,
        )
        user.set_password(password)
        user.save()

        messages.success(request, 'Account created successfully') 

        return redirect('/add_books/')
    
    return render(request, 'register.html')


def logout_page(request):
    logout(request)
    return redirect('/')