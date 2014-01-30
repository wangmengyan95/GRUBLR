from django import forms
from UserProfile.models import MyUser
from django.contrib.auth import get_user_model
User = get_user_model()


class ProfileForm(forms.Form):
	email=forms.EmailField(label='Email', error_messages={'required':'Email is required'},widget=forms.TextInput(attrs={'placeholder':'Email'}))
	firstName=forms.CharField(label='First Name', error_messages={'required':'First name is required'},widget=forms.TextInput(attrs={'placeholder':'First Name'}))
	lastName=forms.CharField(label='Last Name', error_messages={'required':'Last name is required'},widget=forms.TextInput(attrs={'placeholder':'Last Name'}))
	birthday=forms.DateField(label='Birthday', error_messages={'required':'Birthday is required'},widget=forms.TextInput(attrs={'placeholder':'Birthday'}))
	avatar=forms.ImageField(required=False)

	def clean_email(self):
		email=self.cleaned_data['email']
		if len(User.objects.filter(email=email))>1:
			raise forms.ValidationError("Email has already been taken")
		return email


class RegisterForm(forms.Form):
	userName=forms.CharField(label='User Name', error_messages={'required':'User name is required'})
	email=forms.EmailField(label='Email', error_messages={'required':'Email is required'})
	password=forms.CharField(label='Password', error_messages={'required':'Password is required'})
	password1=forms.CharField(label='Password1', error_messages={'required':'Confirm password is required'})

	def clean_email(self):
		email=self.cleaned_data['email']
		if len(User.objects.filter(email=email))>0:
			raise forms.ValidationError("Email has already been taken")
		return email

	def clean_userName(self):
		userName=self.cleaned_data['userName']
		if len(User.objects.filter(username=userName))>0:
			raise forms.ValidationError("Username has already been taken")
		return userName

	def clean_password1(self):
		password=self.cleaned_data['password']
		password1=self.cleaned_data['password1']
		if(password!=password1):
			raise forms.ValidationError("Passwords are not match")
		return password1


class ChangePasswordForm(forms.Form):
	oldPassword=forms.CharField(label='oldPassword', error_messages={'required':'Old Password is required'})
	newPassword=forms.CharField(label='newPassword', error_messages={'required':'New Password is required'})
	newPassword1=forms.CharField(label='newPassword1', error_messages={'required':'Confirm password is required'})

	def __init__(self, user, *args, **kwargs):
		super(ChangePasswordForm, self).__init__(*args, **kwargs)
		self._user=user;

	def clean_newPassword1(self):
		password=self.cleaned_data['newPassword']
		password1=self.cleaned_data['newPassword1']
		if(password!=password1):
			raise forms.ValidationError("New Passwords are not match")
		return password1

	def clean_oldPassword(self):
		password=self.cleaned_data['oldPassword']
		if(self._user.check_password(password)!=True):
			raise forms.ValidationError("Old Password is not correct")
		return password
