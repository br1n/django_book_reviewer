# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Author, Book, Review
# Create your views here.

def index(request):
    if 'id' in request.session:
        return redirect('/dashboard') #denies access when logged in
    
    else:
        return render(request, 'main/index.html')

def register(request):
    if request.method != 'POST': 
        return redirect('/')
    

    valid, response = User.objects.validate_and_create_user(request.POST)
    if valid:
        request.session['id'] = response.id
        return redirect('/') #if valid, login
    else:
        for error in response:
            messages.error(request, error)
    return redirect('/')

def login(request):
    if request.method != 'POST':
        return redirect('/')

    valid, response = User.objects.validate_login(request.POST)
    if valid == False:
        for error in response:
            messages.error(request, error)
        return redirect('/')
    else:
        request.session['id'] = response.id
        return redirect('/dashboard')

def dashboard(request):
    if not 'id' in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['id'])
    latest_three = Review.objects.all().order_by("-created_at")[0:3]
    ids =[]
    for review in latest_three:
        ids.append(review.book.id)
    
    context = {
        "user" : user,
        "latest_three": latest_three,
        "other_books": Book.objects.exclude(id__in=ids)
    }

    return render(request, "main/dashboard.html", context)

def add(request):
    if not 'id' in request.session:
        return redirect('/')  
    user = User.objects.get(id=request.session['id'])
    context = {
        "authors": Author.objects.all(),
    } #this retrieves all "authors"{%for author in AUTHORS%} added to access as 'select option'

    return render(request, "main/add.html", context)

def create(request):#process in data before creating new data in DB 
    print request.POST #this will test are getting form data redirect back to add page

    
    #author verification/create
    author_name = request.POST['new_author'] #retrieves new_author from 'new author' input text field on add page
    if author_name == "": #if 'new_author' text field is blank...
        author_name = request.POST['old_author'] #grabs from 'old_author' select options
    authors = Author.objects.filter(name=author_name)
    #searches db for existing 'authors'
    if len(authors) == 0: #if we dont find author in db...
         author = Author.objects.create(name=author_name) #this creates author
    else:
        author = authors[0] 

    #book verification/create
    book_title = request.POST['title'] #retrieves book title from 'title' input text field on add
    books = Book.objects.filter(title=book_title) #looks for book title in Book table with title of 'book_title'
    if len(books) == 0: #if we dont find book in db...
         book = Book.objects.create(title=book_title, author=author) #this creates book
    else:
        book = books[0]

    user = User.objects.get(id=request.session['id']) #user in session
    Review.objects.create(
        book = book,
        user = user,
        content = request.POST['review'], #grabs from 'review' content from review: text area
        rating = request.POST['rating']
    )
    return redirect('/books/{}'.format(book.id))

def show(request, book_id):
    if not 'id' in request.session:
        return redirect('/')

    context = {
        "book": Book.objects.get(id=book_id), #the book shown is the book with current ID.
    }
    return render(request, 'main/showbook.html', context)

def reviews_create(request, book_id):
    user = User.objects.get(id=request.session['id']) #user in session
    book = Book.objects.get(id=book_id)
    Review.objects.create(
        book = book,
        user = user,
        content = request.POST['review'], #grabs from 'review' content from review: text area
        rating = request.POST['rating']
    )
    return redirect('/books/{}'.format(book.id))

def reviews_delete(request, review_id):
    user = User.objects.get(id=request.session['id']) #user in session
    review = Review.objects.get(id=review_id)
    book_id = review.book.id
    if review.user == user:
        review.delete()
    return redirect('/books/{}'.format(book_id))

def logout(request):
    request.session.clear()
    return redirect('/')

def user(request, user_id):
    if not 'id' in request.session:
        return redirect('/')
        
    user = User.objects.get(id=user_id)
    # reviews = Review.objects.all()
    
    context = {
        "user": user,
    }
    return render(request, "main/user.html", context)
