from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required

def login(request):
    if request.method == 'POST':
        user = auth.authenticate(
            username = request.POST['uname'],
            password = request.POST['psw']
        )
        if user is not None:
            auth.login(request,user)
            return redirect('loginview')
        else:
            error = 'User not found'
            context = {
                'error': error
            }
            return render(request, "login/LoginPage.html", context)
    return render(request, "login/LoginPage.html")

@login_required
def logout(request):
    auth.logout(request)
    return redirect('home')
# Create your views here.

