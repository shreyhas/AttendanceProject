from django.shortcuts import render, redirect

def home(request):

    print(request.user)

    if request.user.is_authenticated:
        return redirect('loginview')
    else:
        return render(request, "home/Home.html")





# Create your views here.
