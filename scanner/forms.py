from django import forms

class ScannerForm(forms.Form):
    TARGET_CHOICES = [
        ('ip', 'IP Address'),
        ('domain', 'Domain'),
        ('subdomain', 'Sub-Domain'),
        ('cidr', 'CIDR'),
        ('url', 'URL'),
    ]
    
    target = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Your Target'}),
        help_text="You can enter any one of the following type of target: IP Address, Domain, Sub-Domain, CIDR, or URL."
    )
    target_type = forms.ChoiceField(
        choices=TARGET_CHOICES,
        widget=forms.RadioSelect,
        help_text="Select the type of target you're entering."
    )