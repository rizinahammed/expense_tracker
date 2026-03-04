from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Category, Transaction


class SignupForm(UserCreationForm):
    password1 = forms.CharField(
        label='Password',
        required=True,
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        error_messages={'required': 'Password is required'},
        help_text='',
    )
    password2 = forms.CharField(
        label='Confirm Password',
        required=True,
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        error_messages={'required': 'Confirmation is required'},
        help_text='',
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username',)

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords do not match')

        return password2

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Category name'}),
        }

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount', 'type', 'category', 'date', 'description']
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '0.00'}),
            'type': forms.RadioSelect(),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'e.g., Coffee at Starbucks, Salary payment, etc.'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['type'].choices = [
            choice for choice in self.fields['type'].choices if choice[0] != ''
        ]
        if user:
            self.fields['category'].queryset = Category.objects.filter(user=user)
        self.fields['category'].empty_label = 'Select category'
        # Set default date to today if not editing existing transaction
        if not self.instance.pk:
            self.fields['date'].initial = timezone.now().date()
            self.fields['type'].initial = 'expense'  # Default to expense