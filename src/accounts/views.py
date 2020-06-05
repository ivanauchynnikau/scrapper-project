from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.contrib import messages
from accounts.forms import UserLoginForm, UserRegistrationForm, UserUpdateForm


def login_view(request):
    form = UserLoginForm(request.POST or None)

    if form.is_valid():
        data = form.cleaned_data

        email = data.get('email')
        password = data.get('password')

        user = authenticate(request, email=email, password=password)

        login(request, user)
        return redirect('home')
    
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


def register_view(request):
    form = UserRegistrationForm(request.POST or None)  # зачем тут None
    if form.is_valid():
        # commit=False - means do not save in DB
        new_user = form.save(commit=False)
        new_user.set_password(form.cleaned_data['password'])
        new_user.save()
        messages.success(request, 'Profile was created.')
        return render(request, 'accounts/register_done.html',
                      {'new_user': new_user})
    return render(request, 'accounts/register.html', {'form': form})


def update_view(request):
    if request.user.is_authenticated:
        user = request.user
        if request.method == 'POST':
            form = UserUpdateForm(request.POST)
        else:
            form = UserUpdateForm(initial={'city': user.city, 'language': user.language,
                                           'send_email': user.send_email})
            return render(request, 'accounts/update.html',
                          {'form': form})
    else:
        return redirect('accounts:login')
