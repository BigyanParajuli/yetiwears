from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail
from Yetiwares import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth import authenticate, login, logout
from . tokens import generate_token

# Create your views here.
def home(request):
    return render(request, "authentication/index.html")

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        
        if User.objects.filter(username=username):
            messages.error(request, "Username already exist! Please try some other username.")
            return redirect('home')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email Already Registered!!")
            return redirect('home')
        
        if len(username)>20:
            messages.error(request, "Username must be under 20 charcters!!")
            return redirect('home')
        
        if pass1 != pass2:
            messages.error(request, "Passwords didn't matched!!")
            return redirect('home')
        
        if not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric!!")
            return redirect('home')
        
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.is_active = True  # Set user as active immediately after creation
        myuser.save()
        messages.success(request, "Your Account has been created successfully!!")

        # # You can still send a welcome email if you want, just remove the confirmation part
        # # Welcome Email
        # subject = "Welcome to GFG- Django Login!!"
        # message = "Hello " + myuser.first_name + "!! \n" + "Welcome to GFG!! \nThank you for visiting our website.\n\nThanking You\nAnubhav Madhav"        
        # from_email = settings.EMAIL_HOST_USER
        # to_list = [myuser.email]
        # send_mail(subject, message, from_email, to_list, fail_silently=True)
        
        return redirect('signin')
        
    return render(request, "authentication/signup.html")


def activate(request,uidb64,token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError,ValueError,OverflowError,User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser,token):
        myuser.is_active = True
        # user.profile.signup_confirmation = True
        myuser.save()
        login(request,myuser)
        messages.success(request, "Your Account has been activated!!")
        return redirect('signin')
    else:
        return render(request,'activation_failed.html')


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']
        
        user = authenticate(username=username, password=pass1)
        
        if user is not None:
            login(request, user)
            fname = user.first_name
            # messages.success(request, "Logged In Sucessfully!!")
            return render(request, "authentication/index.html",{"fname":fname})
        else:
            messages.error(request, "Bad Credentials!!")
            return redirect('home')
    
    return render(request, "authentication/signin.html")


def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return redirect('home')


from .models import Review

def feedback(request):
    if request.method == 'POST':
        # If the form is submitted
        rating = request.POST.get('rating')  # Get the rating value from the form
        review_text = request.POST.get('review_text')  # Get the review text from the form

        # Create a new Review object and save it to the database
        review = Review.objects.create(rating=rating, review_text=review_text)

        # Optionally, you can add a success message or redirect the user to a different page
        messages.success(request, "Feedback saved successfully!")
        return redirect('home')  # Redirect to the home page after saving feedback

    # If the request is a GET request or the form submission fails, render the feedback form
    return render(request, 'authentication/feedback.html')

def submit_feedback(request):
    if request.method == 'POST':
        rating = request.POST.get('rating')  # Get the rating value from the form
        review_text = request.POST.get('review_text')  # Get the review text from the form

        # Create a new Review object and save it to the database
        review = Review.objects.create(rating=rating, review_text=review_text)
        review.save()

        # Optionally, you can add a success message or redirect the user to a different page
        return redirect('home')
    else:
        # Handle GET requests if needed
        return HttpResponse("Method not allowed")
