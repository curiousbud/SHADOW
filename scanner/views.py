from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import get_object_or_404
from .tasks import run_scan
from .models import Target,Vulnerability, ScanReport, Notification
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
    return redirect('login')

# Registration View
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # This should save the user
            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('login')  # Redirect to login after successful registration
        else:
            # Add this to display form errors in case something is wrong
            print(form.errors)  # Debugging step to see why form might be invalid
            messages.error(request, 'Registration failed. Please correct the errors.')
    else:
        form = UserCreationForm()

    return render(request, 'registration/signup.html', {'form': form})

@login_required
def index(request):
    return render(request,'scanner/index.html')

@login_required
def vulnerability(request):
    vulnerabilities = Vulnerability.objects.filter(target__user=request.user)
    return render(request, 'scanner/vulnerability.html', {'vulnerabilities': vulnerabilities})

@login_required
def target(request):
    targets = Target.objects.filter(user=request.user)
    
    if request.method == 'POST':
        # Handle new target submission
        target_input = request.POST.get('url', '').strip()
        
        if target_input:
            # Create new target
            target = Target.objects.create(
                user=request.user,
                # Determine if input is URL, IP, or domain and set accordingly
                url=target_input if target_input.startswith(('http://', 'https://')) else None,
                ip_address=target_input if is_valid_ip(target_input) else None,
                domain=target_input if not (target_input.startswith(('http://', 'https://')) or is_valid_ip(target_input)) else None
            )
            
            try:
                # Start the scan immediately for new targets
                run_scan.delay(target.id)
                messages.success(request, f'Target added and scan started for {target_input}')
            except Exception as e:
                messages.error(request, f'Target added but failed to start scan: {str(e)}')
            
            return redirect('target')
        else:
            messages.error(request, 'Please provide a valid target')
    
    return render(request, 'scanner/target.html', {'targets': targets})

# Helper function to validate IP addresses
def is_valid_ip(ip_str):
    try:
        # Split the IP string into octets
        parts = ip_str.split('.')
        
        # Check if we have exactly 4 parts
        if len(parts) != 4:
            return False
            
        # Check that each number is between 0 and 255
        return all(0 <= int(part) <= 255 for part in parts)
    except (AttributeError, TypeError, ValueError):
        return False


@login_required
def report(request):
    reports = ScanReport.objects.filter(target__user=request.user)
    return render(request, 'scanner/report.html', {'reports': reports})

@login_required
def notify(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_date')
    return render(request, 'scanner/notify.html', {'notifications': notifications})

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

@login_required
def start_scan(request, target_id):
    # Get the target and verify it belongs to the requesting user
    target = get_object_or_404(Target, id=target_id, user=request.user)
    
    try:
        # Start the scan using Celery task
        run_scan.delay(target_id)
        messages.success(request, f'Scan started for {target.url or target.ip_address or target.domain}')
    except Exception as e:
        messages.error(request, f'Failed to start scan: {str(e)}')
    
    # Redirect back to the targets page
    return redirect('target')





