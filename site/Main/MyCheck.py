from django.core.validators import email_re
from django.contrib.auth.models import User
from django.contrib import auth
from UserProfile.models import MyUser 
from django.contrib.auth import get_user_model
User = get_user_model()

def checkValidEmail(email):
    return True if email_re.match(email) else False

def chechUserNameIntegrity(request):
	errors={}	
	errors['type']=[];
	errors['message']=[];

	if not 'userName' in request.POST or not request.POST['userName']:
		errors['type'].append('userName')
		errors['message'].append('User name is required')

	if 'userName' in request.POST and request.POST['userName'] \
		and len(User.objects.filter(username=request.POST['userName']))>0:
		errors['type'].append('userName')
		errors['message'].append('User name is already taken')	

	return errors


def checkRegisterForm(request):

	# User=MyUser
	#!!!!!!!!!!!!!!

	errors={}	
	errors['type']=[];
	errors['message']=[];

	# p=User.objects.filter(username=request.POST['userName'])
	# # assert False
	# errors['type'].append(len(User.objects.filter(username=request.POST['userName'])))
	# errors['type'].append(len(User.objects.filter(username=request.POST['userName']))>0)
	# errors['type'].append(checkIntegrity(request.POST['userName'], 'username', User)==False)
	# errors['type'].append(checkIntegrity(request.POST['userName'], 'username', User) is False)
	# return errors

	if not 'userName' in request.POST or not request.POST['userName']:
		errors['type'].append('userName')
		errors['message'].append('User name is required')
		# errors['userNameNotExist']='User name is required'

	if not 'password' in request.POST or not request.POST['password']:
		errors['type'].append('password')
		errors['message'].append('Password is required')
		# errors['passwordNotExist']='Password is required'
	if not 'password1' in request.POST or not request.POST['password1']:
		errors['type'].append('password1')
		errors['message'].append('Confirm password is required')
		#errors['password1NotExist']='Confirm password is required'

	if not 'email' in request.POST or not request.POST['email']:
		errors['type'].append('email')
		errors['message'].append('Email address is required')
		# errors['emailNotExist']='Email address is required'

	if 'email' in request.POST and request.POST['email'] and checkValidEmail(request.POST['email'])==False:
		errors['type'].append('email')
		errors['message'].append('Email address is not valid')
		# errors['emailNotFormat']='Email is not valid'	

	if 'password' in request.POST and 'password1' in request.POST \
		and request.POST['password'] and request.POST['password1'] \
		and request.POST['password'] != request.POST['password1']:
		errors['type'].append('password1')
		errors['message'].append('Passwords not match')
		#errors['passwordNotMatch']='Passwords not match'

	if 'userName' in request.POST and request.POST['userName'] \
		and len(User.objects.filter(username=request.POST['userName']))>0:
		errors['type'].append('userName')
		errors['message'].append('User name is already taken')		
		#errors['userNameNotIntegrity']='User name is already taken'

	if 'email' in request.POST and request.POST['email'] \
		and len(User.objects.filter(username=request.POST['email']))>0:
		errors['type'].append('email')
		errors['message'].append('Email is already taken')	

	return errors

def checkProfileForm(request):
	errors={}	
	errors['type']=[];
	errors['message']=[];

	if not 'email' in request.POST or not request.POST['email']:
		errors['type'].append('email')
		errors['message'].append('Email address is required')	

	if 'email' in request.POST and request.POST['email'] and checkValidEmail(request.POST['email'])==False:
		errors['type'].append('email')
		errors['message'].append('Email address is not valid')

	if 'email' in request.POST and request.POST['email'] \
		and len(User.objects.filter(username=request.POST['email']))>0:
		errors['type'].append('email')
		errors['message'].append('Email is already taken')	
		

	if not 'firstName' in request.POST or not request.POST['firstName']:
		errors['type'].append('firstName')
		errors['message'].append('First name is required')

	if not 'lastName' in request.POST or not request.POST['lastName']:
		errors['type'].append('lastName')
		errors['message'].append('Last name is required')

	if not 'birthday' in request.POST or not request.POST['birthday']:
		errors['type'].append('birthday')
		errors['message'].append('Birthday is required')

	return errors