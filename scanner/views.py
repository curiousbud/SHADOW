from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.http import require_POST
from .forms import ScannerForm,LoginForm

# Create your views here.

# Login View
def login_view(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')  # Redirect to your dashboard
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'registration/login.html', {'form': form})  # Render the login template

# Logout View
@login_required
def logout_view(request):
    logout(request)  # Log out the user
    messages.success(request, "You have been logged out.")
    return redirect('login',{'form': form})

# Registration View
def register_view(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = User(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email']
            )
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('registration/login.html', {'form': form})  # Redirect to login page
    else:
        form = UserCreationForm()
    
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def index(request):
    return render(request,'scanner/index.html')

@login_required
def vulnerability(request):
    return render(request,'scanner/vulnerability.html')

@login_required
def target(request):
    return render(request,'scanner/target.html')

@login_required
def report(request):
    return render(request,'scanner/report.html')

@login_required
def notify(request):
    return render(request,'scanner/notify.html')

@login_required
def profile(request):
    return render(request,'partials/profile.html')

@login_required
def settings(request):
    return render(request,'partials/settings.html')

@login_required
def scan(request):
    if request.method == 'POST':
        form = ScannerForm(request.POST)
        if form.is_valid():
            # Process the form data
            target = form.cleaned_data['target']
            target_type = form.cleaned_data['target_type']
            # Add your logic here to handle the submitted data
    else:
        form = ScannerForm()
    
    return render(request, 'scanner/scan.html', {'form': form})

