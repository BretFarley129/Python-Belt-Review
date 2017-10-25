# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages

import bcrypt

# Create your views here.

def index(request):
    return render(request,'belt/index.html')



def register(request):
    name = request.POST['name']
    alias = request.POST['alias']
    email = request.POST['email']
    password = request.POST['password']
    confirm = request.POST['confirm']
    x = {'name': name,'alias': alias, 'email': email, 'password': password, 'confirm': confirm}
    errors = User.objects.validate(x)
    if errors:
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/')
    else:
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        user = User.objects.create(name = name, alias = alias, email = email, password = hashed_password )
        request.session['id'] = User.objects.filter(email=request.POST['email'])[0].id
        return redirect('/books')

def login(request):
    email = request.POST['email']
    password = request.POST['password']
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    try:
        user = User.objects.filter(email = email)[0]
        hash1 = user.password
    except:
        hash1 = request.POST['email']


    x = { 'email': email, 'password': password, 'hash1' : hash1}
    errors = User.objects.validateLogin(x)
    if errors:
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/')
    else:
        request.session['id'] = User.objects.filter(email=request.POST['email'])[0].id
        return redirect('/books')

def books(request):
    context = {}
    context['stuff'] = Review.objects.all()
    print Book.objects.all()
    return render(request,'belt/books.html',context)

def add(request):
    if not request.session['id']:
        messages.add_message(request, messages.INFO, 'You must be logged in to see this content')
        return redirect('/')
    context = {}
    context['stuff'] = Author.objects.all()
    return render(request, 'belt/add.html',context)
def newBook(request):
    title = request.POST['title']
    a1 = request.POST['a1']
    a2 = request.POST['a2']
    review = request.POST['review']
    rating = request.POST['rating']
    context ={}
    if a2:
        Author.objects.create(name = a2)
        p = Author.objects.filter(name = a2)[0]
        author = p
    else:
        p = Author.objects.filter(name = a1)[0]
        author = p

    Book.objects.create(title = title, author = author)
    new_book = Book.objects.filter(title = title)[0]
    print new_book
    currentUser = User.objects.get(id = request.session['id'])

    Review.objects.create(book = new_book, content = review, user = currentUser, rating = rating)

    return redirect('/books')

def showbook(request, number):
    if not request.session['id']:
        messages.add_message(request, messages.INFO, 'You must be logged in to see this content')
        return redirect('/')
    context = {}
    theBook = Book.objects.get(id = number)
    print theBook
    context['book'] = theBook
    context['revs'] = Review.objects.filter(book = theBook)
    return render(request, 'belt/showBook.html',context)
def new(request, number):
    user = User.objects.get(id = request.session['id'])
    book = Book.objects.get(id = number)
    review = request.POST['review']
    rating = request.POST['rating']
    Review.objects.create(book = book, content = review, user = user, rating = rating)
    return redirect('/books/{}'.format(number))
def showuser(request, number):
    if not request.session['id']:
        messages.add_message(request, messages.INFO, 'You must be logged in to see this content')
        return redirect('/')
    context = {}
    theUser = User.objects.get(id = number)
    context['stuff'] = theUser
    context['tot'] = len(Review.objects.filter(user = theUser))
    context['revs'] = Review.objects.filter(user = theUser)
    return render(request, 'belt/showUser.html', context)

def delete(request, number, boo):
    Review.objects.get(id = number).delete()
    return redirect('/books/{}'.format(boo))

def logout(request):
    request.session['id'] = ""
    return redirect('/')