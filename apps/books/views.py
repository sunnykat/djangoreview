from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.db.models import Count
from django.http import HttpResponseRedirect
from .models import Books, Author, Reviews, ReviewManager, BookManager
from ..login.models import User

# Create your views here.
def index(request):
    if 'id' not in request.session:
        messages.error(request, 'Please log in to continue.')
        return redirect(reverse('login:index'))
    context={
    'allbooks':Books.objects.all(),
    'recentreviews':Reviews.objects.all().order_by('-created_at')[:3],
    }

    return render(request, 'books/splash.html', context)

def book(request, b_id):
    if 'id' not in request.session:
        messages.error(request, 'Please log in to continue.')
        return redirect(reverse('login:index'))
    book=Books.objects.get(id=b_id)
    context={
    'book':book,
    'reviews':Reviews.objects.filter(book=book),
    }
    return render(request,'books/book.html', context)

def newbook(request):
    if not request.method == 'POST':
        return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
    u_id=request.session['id']
    book_id=str(Books.objects.addBooks(request.POST,u_id))
    return redirect('./book/'+book_id)

def newreview(request):
    if not request.method == 'POST':
        return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
    u_id=request.session['id']
    Reviews.objects.addReview(request.POST, u_id)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))

def removereview(request, r_id):
    if 'id' not in request.session:
        messages.error(request, 'Please log in to continue.')
        return redirect(reverse('login:index'))
    Reviews.objects.deleteReview(r_id)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))

def add(request):
    if 'id' not in request.session:
        messages.error(request, 'Please log in to continue.')
        return redirect(reverse('login:index'))
    context={
    'authors':Author.objects.all(),
    }
    return render(request, 'books/add.html', context)

def user(request,u_id):
    if 'id' not in request.session:
        messages.error(request, 'Please log in to continue.')
        return redirect(reverse('login:index'))
    user=User.objects.get(id=u_id)
    context={
        'user':user,
        'count':Reviews.objects.filter(user=user).annotate(total=Count('id')),
        'reviews':Reviews.objects.filter(user=user),
    }
    return render(request, 'books/user.html', context)
