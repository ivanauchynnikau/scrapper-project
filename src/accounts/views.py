from django.contrib.auth import authenticate, login, logout, get_user_model
from django.shortcuts import redirect, render
from django.contrib import messages
from accounts.forms import UserLoginForm, UserRegistrationForm, UserUpdateForm

User = get_user_model()

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
            if form.is_valid():
                date = form.cleaned_data

                user.city = date['city']
                user.language = date['language']
                user.send_email = date['send_email']
                user.save()
                messages.success(request, 'Profile was updated.')
                return render(request, 'accounts/update.html', {'form': form})

        form = UserUpdateForm(initial={'city': user.city, 'language': user.language,
                                       'send_email': user.send_email})
        return render(request, 'accounts/update.html', {'form': form})
    else:
        return redirect('accounts:login')


def delete_view(request):
    if request.user.is_authenticated:
        user = request.user

        if request.method == 'POST':
            qs = User.objects.get(pk=user.pk)
            qs.delete()
            messages.success(request, 'Profile was deleted.')

    return redirect('home')
