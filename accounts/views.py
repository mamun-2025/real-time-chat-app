from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout 
from django.contrib.auth.forms import AuthenticationForm 
from .forms import SignUpForm 
from django.contrib import messages


# Sign up view 
def signup_view(request):
   if request.method == 'POST':
      form = SignUpForm(request.POST)
      if form.is_valid():
         user = form.save()
         login(request, user)
         messages.success(request, 'Sign up successfully!')
         return redirect('chat_room')
      else:
         messages.error(request, 'Sign up failed. Please check form errors.')
   else:
      form = SignUpForm()
   return render(request, 'registration/signup.html', {'form': form})


# Login view 
def login_view(request):
   if request.method == 'POST':
      form = AuthenticationForm(request, data=request.POST) 
      if form.is_valid():
         username = form.cleaned_data.get('username')
         password = form.cleaned_data.get('password')
         user = authenticate(username=username, password=password)
         if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {username}!")
            return redirect('chat_room')
         else:
            messages.error(request, 'Invalid username or password. Please try again.')
      else:
         messages.error(request, 'Invalid credentials. Please check form error.')
   else:
      form = AuthenticationForm()
   return render(request, 'registration/login.html', {'form': form})


# Logout view 
def logout_view(request):
   logout(request)
   messages.info(request, "yYou have successfully logged out.")
   return redirect('login')




