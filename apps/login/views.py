from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from .models import User, userManager
# Create your views here.
def index(request):
    return render(request, 'login/index.html')

def process(request):
    error=0
    if not userManager.lengthCheck(request.POST['fname'],request.POST['lname'],request.POST['email'], request.POST['pass1']):
        messages.error(request, 'Please fill out all fields.')
        error=1
    if not userManager.validEmail(request.POST['email']):
        messages.error(request, 'Email address is invalid.')
        error=1
    if not userManager.existingEmail(request.POST['email']):
        messages.error(request, 'Email addres already exists.')
        error=1
    if not len(request.POST['pass1'])>7:
        messages.error(request,'Password must be at least 8 characters')
        error=1
    if not request.POST['pass1'] == request.POST['pass2']:
        messages.error(request, 'Passwords must match')
        error=1
    if error:
        return redirect('/')
    userManager.addUser(str(request.POST['fname']),str(request.POST['lname']),str(request.POST['email']),str(request.POST['pass1']))

    user=User.objects.get(email=str(request.POST['email']))
    request.session['id']=user.pk
    return redirect(reverse('books:index'))

def login(request):
    error=0
    if not userManager.validEmail(str(request.POST['email'])):
        messages.error(request, 'A vaild email is required to login.')
        error=1
    if userManager.existingEmail(str(request.POST['email'])):
        messages.add_message(request, messages.ERROR, 'Email or password is incorrect.')
        error=1
    if error:
        return redirect('/')
    if not userManager.passCheck(request.POST['email'],request.POST['pass']):
        messages.add_message(request, messages.ERROR, 'Email or password is incorrect.')
        error=1
    if error:
        return redirect('/')
    else:
        user=User.objects.get(email=request.POST['email'])
        request.session['id']=user.pk
        messages.add_message(request, messages.SUCCESS, 'Welcome,'+user.fname+'!')
        return redirect(reverse('books:index'))


def logout(request):
    request.session.clear()
    return redirect(reverse('login:index'))
