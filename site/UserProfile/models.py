from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import os
from django.conf import settings



class MyUserManager(BaseUserManager):
	def create_user(self, username, email, password=None):
		if not email:
			raise ValueError('User must have an email address')
		if not username:
			raise ValueError('User must have a user name')

		user =self.model(
			email=MyUserManager.normalize_email(email),
			username=username,
		)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, uesrname, email, password=None):
		user =self.model(
			email=MyUserManager.normalize_email(email),
			username=username,
		)
		user.set_password(password)
		user.isAdmin=True
		user.save(using=self._db)
		return user	

def generate_new_filename(instance, filename):
    ext = filename.split('.')[-1]
    fileName="%s.%s" %(str(instance.username),ext)

	#delete exist file
	# fullFileName=os.path.join(str(settings.MEDIA_ROOT),'avatar',fileName)
	# if os.path.exists(fullFileName):
	# 	os.remove(fullFileName)

    return os.path.join('avatar', fileName)

class MyUser(AbstractBaseUser):
	username=models.CharField(max_length=100, unique=True)
	firstName=models.CharField(max_length=30, blank=True)
	lastName=models.CharField(max_length=30, blank=True)
	email=models.EmailField(unique=True)
	isAdmain=models.BooleanField(default=False)
	birthday=models.DateField(null=True);
	avatar=models.ImageField(blank=True, upload_to=generate_new_filename,default="avatar/default.jpg")

	USERNAME_FIELD='username'
	REQUIRED_FIELDS=['email']

	objects = MyUserManager()



class MyUserFriend(models.Model):
	user=models.ForeignKey(MyUser, related_name="MyUserFriend_user")
	friend=models.ForeignKey(MyUser, related_name="MyUserFriend_friend")

class MyUserBlock(models.Model):
	user=models.ForeignKey(MyUser, related_name="MyUserBlock_user")
	block=models.ForeignKey(MyUser, related_name="MyUserBlock_block")
