from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.db.models import fields
from django import forms
from .models import CustomUser                                   #UserProfile
from django.contrib.auth import get_user_model

User1 = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput, label='Password')
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('email',)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User1.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("Email is already used for another user.")
        return email

    def clean(self):
        '''
        Verify both passwords match.
        '''
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 is not None and password1 != password2:
            self.add_error("password2", "Your passwords must match")
        return cleaned_data

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.save()
        # UserProfile.objects.create(user=user)
        return user
