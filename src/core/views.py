from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from django.shortcuts import render


def index(request):
    """
    Displays the home page.
    """
    return render(request, 'index.html')


def signup(request):
    """
    Displays and receives a user registration form.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    return render(request, 'signup.html', {'form': UserCreationForm()})


def logout_view(request):
    """
    Logs the user out and redirects to the home page.
    """
    logout(request)
    return redirect('/')
