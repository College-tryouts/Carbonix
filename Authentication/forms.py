# carbontracker/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, ROLE_CHOICES
from emissions.models import Company

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(choices=ROLE_CHOICES)
    company = forms.ModelChoiceField(queryset=Company.objects.all(), required=False)
    phone = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'role', 'company', 'phone')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            profile = Profile.objects.create(
                user=user,
                role=self.cleaned_data['role'],
                company=self.cleaned_data.get('company'),
                phone=self.cleaned_data.get('phone')
            )
        return user
