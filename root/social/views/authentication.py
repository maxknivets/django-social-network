from django.contrib.auth import authenticate, login, logout
from social.forms import Sign_up_form
from django.shortcuts import render, redirect
from social.models import Profile

def signup(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        form = Sign_up_form(request.POST)
        if form.is_valid():
            form.save()
            profile = Profile(user=request.user)
            profile.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = Sign_up_form()
    return render(request, 'registration/signup.html', {'form': form})

def logout(request):
    logout(request)
    return redirect('/login')

def validate_username(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(data)