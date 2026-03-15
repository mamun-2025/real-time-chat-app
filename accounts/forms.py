
from django import forms 
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm 

class SignUpForm(UserCreationForm):
   username =forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'input-field'}))
   email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'input-field'}))
   password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input-field'}))
   password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input-field'})) 

   class Meta:
      model = User
      fields = ('username', 'email', 'password1', 'password2')
     

     