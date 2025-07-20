from django.shortcuts import render,redirect
from django.http import HttpResponse
from Base_app.models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from Base_app.middleware import auth

# Create your views here.

def HomeView(request):
    categories = Item_list.objects.prefetch_related('Name')
    review = Feedback.objects.all()
    reviews = Feedback.objects.all().order_by('-id')[:10]

    return render(request, 'home.html', {'categories': categories, 'review':review, 'reviews':reviews})

def AboutView(request):
    data = AboutUs.objects.all()
    return render(request,'about.html',{'data':data})


def MenuView(request):
    categories = Item_list.objects.prefetch_related('Name')
    return render(request,'menu.html',{'categories':categories})
 

def BookTableView(request):
    if request.method == 'POST':
        name = request.POST.get('user_name')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('user_email')
        total = request.POST.get('total_person')
        booking_date = request.POST.get('booking_date')

        if name!='' and phone_number!='' and email!='' and total!='' and booking_date!='':
            try:
                data = Booktable(Name=name, Phone_number=phone_number, Email=email, Total_person=total, Booking_date=booking_date)

                print(data)
                data.save()
            except ValueError:
                return HttpResponse("Please enter valid numeric values")

        else:
            return HttpResponse("All fields are required")    

    return render(request,'book_table.html')


def FeedbackView(request):
    if request.method == 'POST':
        name = request.POST.get('user_name')
        rating = request.POST.get('user_rating')
        description = request.POST.get('user_description')

        if name and rating and description:
            try:
                data = Feedback(
                    User_name=name,
                    Rating=int(rating),
                    Description=description,
                )
                print(data)
                data.save()
                return redirect('Home')
            except ValueError:
                return HttpResponse("Please enter valid numeric values.")
        else:
            return HttpResponse("All fields are required.")

    return render(request,'feedback.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        if not username or not password:
            messages.error(request, 'Please fill in all fields.')
            return redirect('login')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Change 'home' to your actual route name
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('login')

    return render(request, 'login_page.html')


def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password1 = request.POST.get('password1', '').strip()
        password2 = request.POST.get('password2', '').strip()

        print("Request method:", request.method)
        print("POST data:", username, email)

        # Basic field validation
        if not username or not email or not password1 or not password2:
            messages.error(request, "All fields are required.")
            return redirect('register')

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect('register')  # changed from 'login' to 'register'

        try:
            user = User.objects.create_user(username=username, email=email, password=password1)
            user.save()
            messages.success(request, "Account created successfully. Please log in.")
            return redirect('login')
        except Exception as e:
            messages.error(request, f"Error creating account: {str(e)}")
            return redirect('register')

    return render(request, 'register.html')


@auth
def dashboard_view(request):
    return render(request, 'dashboard.html')

def logout_view(request):
    logout(request)
    return redirect('login')