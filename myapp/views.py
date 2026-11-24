from django.shortcuts import render, redirect, get_object_or_404
from myapp.models import *
#Authentication Imports
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

# Create your views here.

def error(request):
    return render(request, '404.html')

def details(request):
    return render(request, 'blog-details.html')

def blog(request):
    return render(request, 'blog.html')

def index(request):
    
    if request.method == 'POST':
        mycontact = Contact(
         name = request.POST['name'],
         email = request.POST['email'],
         subject = request.POST['subject'],
         message = request.POST['message'],
        )
        mycontact.save()
        return redirect('/')
    else:
        return render(request, 'index.html')

        
def delete(request, id):
    contactinfo = Contact.objects.get(id=id)
    contactinfo.delete()
    return redirect('/show')
       
def show(request):
    all = Contact.objects.all()
    return render(request, 'show.html', {'all': all})
   
    
def portfolio(request):
    return render(request, 'portfolio-details.html')

def service(request):
    return render(request, 'service-details.html')

def starter(request):
    return render(request, 'starter-page.html')


def edit(request, id):
    editappointment = get_object_or_404(Contact, id=id)
    if request.method == 'POST':
        editappointment.name = request.POST['name']
        editappointment.email = request.POST['email']
        editappointment.subject = request.POST['subject']
        editappointment.message = request.POST['message']
        editappointment.save()
        return redirect('/show')
    else:
        return render(request, 'edit.html')
    

def register(request):
    if request.method == 'POST':

        print("FORM DATA RECEIVED:", request.POST)

        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')

        if not username or not password or not confirm_password:
            messages.error(request, "Please fill in all fields.")

        elif password == confirm_password:
            try:
                user = User.objects.create_user(
                    username=username,
                    password=password
                )

                messages.success(request, "Registration successful!")
                return redirect('/login/')

            except Exception as e:
                messages.error(request, f"Registration failed: {e}")

        else:
            messages.error(request, "Passwords do not match.")

    return render(request, 'register.html')



def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        # Check if the user exists
        if user is not None:
            # login(request, user)
            login(request,user)
            messages.success(request, "You are now logged in!")
            # Admin
            if user.is_superuser:
                return redirect('/show')

            # For Normal Users
            return redirect('/index')
        else:
            messages.error(request, "Invalid login credentials")

    return render(request, 'login.html')
    
