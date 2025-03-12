from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import SignUpForm

# Create your views here.


# --------- Registrations ----------

def sign_in(request):
    return render(request, 'register/sign_in.html')

def sign_up(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            form.save()
            # user = form.save(commit=False)  # Save user but don't commit yet
            # user.save()  # Now save user
            # login(request, user)  # Auto-login user
            return redirect("sign_in")  # Redirect after successful signup
    else:
        form = SignUpForm()
    
    return render(request, "register/sign_up.html", {"form": form})
