from django import forms

class TestForm(forms.Form):
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

    # birthdate = forms.DateField(label='Birthdate', widget=forms.SelectDateWidget(years=range(1900, 2023)))
    # resume = forms.FileField(label='Resume', widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))