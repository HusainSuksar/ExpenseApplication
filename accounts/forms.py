from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from accounts.models import User


class CustomUserAdminCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.Meta.required:
            self.fields[field].required = True

    class Meta:
        model = User
        fields = ('email', 'birth_date', 'first_name', 'last_name', 'image', 'address',
                  'country', 'phone', 'gender', 'username', 'is_active', 'type')
        required = ('email', 'birth_date', 'first_name', 'last_name', 'image', 'address',
                    'country', 'phone', 'gender', 'username', 'is_active', 'type')


class UserChangeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.Meta.required:
            self.fields[field].required = True

    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text=password_validation.password_validators_help_text_html(),
        required=False
    )
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text="Enter the same password as before, for verification.",
        required=False
    )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data['password1']:
            user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ('email', 'birth_date', 'first_name', 'last_name', 'image', 'address',
                  'country', 'phone', 'gender', 'username',)
        required = ('email', 'birth_date', 'first_name', 'last_name', 'image', 'address',
                    'country', 'phone', 'gender', 'username',)


class UserAdminChangeForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.Meta.required:
            self.fields[field].required = True

    class Meta:
        model = User
        fields = ('email', 'birth_date', 'first_name', 'last_name', 'image', 'address',
                  'country', 'phone', 'gender', 'username', 'is_active', 'type')
        required = ('email', 'birth_date', 'first_name', 'last_name', 'image', 'address',
                    'country', 'phone', 'gender', 'username', 'is_active', 'type')
