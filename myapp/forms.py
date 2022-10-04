from django import forms
from .models import Order, Student, PasswordReset
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

class RegisterStudentForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'username', 'email', 'password', 'school', 'city', 'interested_in', 'image']

        # ['address', 'city', 'school', 'interested_in']

class InterestForm(forms.Form):
    CHOICES = [('Yes', 1), ('No', 0)]
    interested = forms.CharField(widget=forms.RadioSelect(choices=CHOICES))
    levels = forms.IntegerField(initial = 1)
    comments = forms.CharField(label='Additional Comments', required=False, widget=forms.Textarea)


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['student', 'course', 'levels', 'order_date']
        widgets = {'student': forms.RadioSelect, 'order_date': forms.SelectDateWidget}

class PasswordResetForm(forms.ModelForm):
    class Meta:
        model = PasswordReset
        fields = ('username',)
        widget = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }