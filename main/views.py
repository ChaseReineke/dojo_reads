from django.shortcuts import render, redirect
from .models import User, Author, Book, Review
from django.contrib import messages
import bcrypt

def index(request):
    return render(request, 'index.html')

def register(request):
    errs = User.objects.register_validator(request.POST)
    if len(errs) > 0:
        for msg in errs.values():
            messages.error(request, msg)
        return redirect('/')
    password = request.POST['password']
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    new_user = User.objects.create(
        name=request.POST['name'],
        alias=request.POST['alias'],
        email=request.POST['email'],
        password=hashed,
    )
    request.session['user_id'] = new_user.id
    return redirect('/books')

def login(request):
    errs = User.objects.login_validator(request.POST)
    if errs:
        for msg in errs.values():
            messages.error(request, msg)
        return redirect('/')
    user_list = User.objects.filter(email=request.POST['email'])
    if user_list:
        our_user = user_list[0]
        print(request.POST['password'].encode())
        print(our_user.password)
        if bcrypt.checkpw(request.POST['password'].encode(), our_user.password.encode()):
            print("Passwords match!")
            request.session['user_id'] = our_user.id
            return redirect('/books')
    else:
        messages.error(request, "Login, failed, try again!")
    return redirect('/')

def books(request):
    print('#' * 40)
    all_reviews = Review.objects.all()
    latest_reviews = []
    print(all_reviews)
    for i in range(len(all_reviews)-1, len(all_reviews)-4, -1):
        latest_reviews.append(all_reviews[i])
    print(latest_reviews)
    print('#' * 40)
    logged_in_user = User.objects.get(id=request.session['user_id'])
    context = {
        'all_books': Book.objects.all(),
        'logged_in_user': logged_in_user,
        'latest_reviews': latest_reviews,
    }
    return render(request, 'books.html', context)

def add_book(request):
    context = {
        'all_authors': Author.objects.all()
    }
    return render(request, 'add_book.html', context)

def add_book_and_review(request):
    if len(request.POST['new_author']) == 0:
        my_author = Author.objects.get(id = request.POST['existing_author'])
    else:
        my_author = Author.objects.create(name=request.POST['new_author'])
    logged_in_user = User.objects.get(id=request.session['user_id'])
    new_book = Book.objects.create(
        title=request.POST['title'],
        author=my_author,
        submitter=logged_in_user
    )
    Review.objects.create(
        content=request.POST['content'],
        rating=request.POST['rating'],
        reviewer=logged_in_user,
        book=new_book
    )
    return redirect('/books')

def book_info(request, book_id):
    context = {
        'book': Book.objects.get(id=book_id)
    }
    return render(request, 'book_info.html', context)

def add_review(request):
    my_book = Book.objects.get(id=request.POST['book_id'])
    Review.objects.create(
        content=request.POST['content'],
        rating=request.POST['rating'],
        book=my_book,
        review=User.objects.get(id=request.session['user_id'])
    )
    return redirect(f'/books/{my_book.id}')

def user_info(request, user_id):
    user = User.objects.get(id=user_id)
    unique_book = []
    for review in user.submitted_reviews.all():
        if review.book.title not in unique_book:
            unique_book.append(review.book)
    print(unique_book)
    context = {
        'user': User.objectsget(id=user_id),
        'unique_books': unique_book
    }
    return render(request, "user_info.html", context)

def logout(request):
    request.session.flush()
    return redirect('/')