from django.shortcuts import render
from .forms import ScannerForm

# Create your views here.

def index(request):
    return render(request,'scanner/index.html')

def chart(request):
    return render(request,'scanner/chart.html')

def empty(request):
    return render(request,'scanner/empty.html')
    
def form(request):
    return render(request,'scanner/form.html')

def tab_panel(request):
    return render(request,'scanner/tab-panel.html')

def table(request):
    return render(request,'scanner/table.html')

def empty(request):
    return render(request,'scanner/empty.html')

def ui_elements(request):
    return render(request,'scanner/ui-elements.html')

def base(request):
    return render(request,'scanner/base.html')

def vulnerability(request):
    return render(request,'scanner/vulnerability.html')

def target(request):
    return render(request,'scanner/target.html')

def report(request):
    return render(request,'scanner/report.html')

def notify(request):
    return render(request,'scanner/notify.html')

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

