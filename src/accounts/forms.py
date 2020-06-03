from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import check_password

User = get_user_model()


class UserLoginForm(forms.Form):
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control'}),
                            label='Email')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                               label='Password')

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email').strip()
        password = self.cleaned_data.get('password').strip()

        if email and password:
            qs = User.objects.filter(email=email)

            if not qs.exists():
                raise forms.ValidationError('User with this email is not exists',
                                            code='invalid')

            if not check_password(password, qs[0].password):
                raise forms.ValidationError('Password is incorrect', code='invalid')

            user = authenticate(email=email, password=password)

            if not user:
                raise forms.ValidationError('This account is disabled', code='invalid')

        return super(UserLoginForm, self).clean(*args, **kwargs)








