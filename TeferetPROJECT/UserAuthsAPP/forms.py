from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import EmailInput, TextInput, PasswordInput

from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):

    """
    @class UserForm
    This class handle user creation
    """

    first_name         = forms.CharField(max_length=30, required= True, 
                         widget= TextInput(
                            attrs={"placeholder": "*Your First Name..."}))

    last_name          = forms.CharField(max_length=30, required= True, 
                         widget= TextInput(
                            attrs={"placeholder": "*Your Last Name..."}))

    username           = forms.CharField(max_length=300, required= True, 
                         widget= TextInput(
                            attrs={"placeholder": "*Your User Name..."}))

    password1           = forms.CharField(max_length=300, required= True, 
                         widget= PasswordInput(
                            attrs={"placeholder": "*Your Password...", "class":"password"}))

    password2           = forms.CharField(max_length=300, required= True, 
                         widget= PasswordInput(
                            attrs={"placeholder": "*Confirm your Password...", "class":"password"}))

    email               = forms.EmailField(max_length=300, required=True,
                         widget=  EmailInput(
                            attrs={"placeholder": "*E-mail...","class":"password"}))

    

    class Meta:
        model  = User
        fields = ('username','first_name','last_name','email','password1','password2')

class LoginForm(AuthenticationForm):
    """
    @class LoginForm
    This class handle the authentification of an user
    """
    username           = forms.CharField(max_length=300, required= True, 
                         widget= TextInput(
                            attrs={"placeholder": "*Your User Name...","id":"id_usernameLogin"}))

    password = forms.CharField(max_length=300, required= True, 
                widget= PasswordInput(
                    attrs={"placeholder": "*Your Password...", "class":"password"}))    
   
    class Meta:
        model = User
        fields = ('email','password',)