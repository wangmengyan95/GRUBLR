import json
import random
import string
import datetime
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth
from django.core.context_processors import csrf
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core import serializers
from django.db import IntegrityError
from django.db.models import Q
from UserProfile.models import MyUser, MyUserFriend, MyUserBlock
from Grumblr.models import Grumblr, GrumblrComment, GrumblrThumbUp, GrumblrEncoder
import MyCheck
from mimetypes import guess_type
from UserProfile.forms import ProfileForm, RegisterForm, ChangePasswordForm
from Grumblr.forms import GrumblrForm, GrumblrCommentForm
from django.core.mail import send_mail
import Image
from django.contrib.auth import get_user_model
from django.conf import settings
from os.path import abspath, dirname
User = get_user_model()

def login(request):
		
	if request.user.is_authenticated():
		return HttpResponseRedirect('/home')
	if request.method=='POST':
		userName=request.POST.get('userName')
		passWord=request.POST.get('passWord')
		user=auth.authenticate(username=userName, password=passWord)

		# response_data={}
		# response_data['userName']=userName
		# response_data['passWord']=passWord

		# return HttpResponse(json.dumps(response_data), content_type="application/json")

		if user is not None and user.is_active:
			auth.login(request, user)
			return HttpResponseRedirect("/home")
		else:
			return render_to_response('login.html',{'logInError':'1'},context_instance=RequestContext(request))
	else:
		return render_to_response('login.html',{'logInError':'0'},context_instance=RequestContext(request))


def home(request):

	if not request.user.is_authenticated():
		return HttpResponseRedirect('/login')

	context=getUserStatistics(request.user)

	friendList=getFriendList(request.user)
	friendList.append(request.user)
	blockList=getBlockList(request.user)
	# is friend not block
	grumblrList=list(Grumblr.objects.filter(owner__in=friendList).exclude(owner__in=blockList).order_by('-publishDateTime')[:5])
	context['grumblrList']=grumblrList

	recommendFriendList=getRecommendFriendList(request,request.user)
	context['recommendFriendList']=recommendFriendList
	context['user']=request.user
	return render_to_response('home.html',context,context_instance=RequestContext(request))
	# context={}

	# grumblrList=[];

	# grumblrContentList=Grumblr.objects.order_by('-publishDateTime')[:5]

	# grumblrList=list(Grumblr.objects.order_by('-publishDateTime')[:5])

	# # for grumblrContnet in grumblrContentList:
	# # 	singleGrumblr={}
	# # 	# singleGrumblr['grumblr']=grumblrContnet
	# # 	commentList=list(GrumblrComment.objects.filter(grumblr=grumblrContnet).order_by('-publishDateTime')[:5]);
	# # 	# singleGrumblr['commentList']=commentList
	# # 	# grumblrList.append(singleGrumblr)

	# context['grumblrList']=grumblrList
	# return HttpResponse(json.dumps(context), content_type="application/json")






def relationship(request, type):
	# context={}
	# grumblrList=list(Grumblr.objects.order_by('-publishDateTime')[:5])
	# context['grumblrList']=grumblrList
	# context['user']=request.user
	# return render_to_response('friend.html',context,context_instance=RequestContext(request))
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/login')


	context=getUserStatistics(request.user)
	relationshipList=getUserRelationships(request.user,type)
	print(relationshipList)
	context["relationshipList"]=relationshipList
	context['Followers']=len(getUserRelationships(request.user,"Followers"))
	context['Followings']=len(getUserRelationships(request.user,"Followings"))
	context['Blocks']=len(getUserRelationships(request.user,"Blocks"))

	return render_to_response('relationship.html',context,context_instance=RequestContext(request))


def checkRegisterForm(request):
	# errors=MyCheck.checkRegisterForm(request)
	# return HttpResponse(json.dumps(errors), content_type="application/json")
	if request.method=='POST':
		form=RegisterForm(request.POST)		
	else:
		form=RegisterForm()

	context={}
	print request.POST["userName"]
	print len(User.objects.filter(username=request.POST["userName"]))
	# print form
	print form.errors
	context['errors']=form.errors
	return HttpResponse(json.dumps(form.errors), content_type="application/json")

def register(request):

	if request.method=='POST':
		form=RegisterForm(request.POST)	
		if form.is_valid():
			# create user
			newUser=User.objects.create_user(username=request.POST['userName'], password=request.POST['password'], email=request.POST['email'])
			newUser.save()
			# login
			newUser=auth.authenticate(username=request.POST['userName'], password=request.POST['password'])
			auth.login(request, newUser)

			send_mail('Register Confirmation','Thank you for registing Grumblr','mengyanw@andrew.cmu.edu',[request.POST['email']],fail_silently=False);
	else:
		form=RegisterForm()

	context={}
	context['errors']=form.errors
	return HttpResponse(json.dumps(form.errors), content_type="application/json")	



# def chechUserNameIntegrity(request):
# 	context={}
# 	errors=MyCheck.checkRegisterForm(request)
# 	if(len(errors['type'])>0):
# 		return HttpResponse(json.dumps(False), content_type="application/json")
# 	else:
# 		return HttpResponse(json.dumps(True), content_type="application/json")

def profile(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/login')

	context=getUserStatistics(request.user)
	context['user']=request.user
	context['form']=ProfileForm()



	recommendFriendList=getRecommendFriendList(request,request.user)
	context['recommendFriendList']=recommendFriendList

	return render_to_response('profile.html',context,context_instance=RequestContext(request))

def getProfile(request):
	context={}
	context['userName']=request.user.username
	if request.user:

		context["firstName"]=request.user.firstName;
		context["lastName"]=request.user.lastName;
		context["birthday"]=str(request.user.birthday)
		context["email"]=request.user.email
		context["getProfileSuccess"]=True
		context["avatar"]=request.user.avatar.path
	else:
		context["getProfileSuccess"]=False

	return HttpResponse(json.dumps(context), content_type="application/json")

def editProfileForm(request):
	if request.method=='POST':
		form=ProfileForm(request.POST, request.FILES)
		if form.is_valid():
			p=User.objects.get(username=request.user.username)
			p.firstName=request.POST['firstName']
			p.lastName=request.POST['lastName']
			p.birthday=request.POST['birthday']
			p.email=request.POST['email']
			if request.FILES['avatar']:
				p.avatar=request.FILES['avatar']			
			p.save()			
	else:
		form=ProfileForm()


	context={}
	# p=User.objects.get(username=request.user.username)
	# context['image']=settings.MEDIA_URL+p.avatar.url
	context['errors']=form.errors
	return HttpResponse(json.dumps(form.errors), content_type="application/json")

def selectCertainGrumblar(request, type):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/login')

	grumblrList=[];
	context={}
	if(type=='all'):
		friendList=getFriendList(request.user)
		friendList.append(request.user)
		blockList=getBlockList(request.user)
		# is friend not block
		grumblrList=list(Grumblr.objects.filter(owner__in=friendList).exclude(owner__in=blockList).order_by('-publishDateTime')[:5])


	elif(type=='my'):
		grumblrList=list(Grumblr.objects.filter(Q(owner=request.user)).order_by('-publishDateTime')[:5])
	elif(type=='others'):
		friendList=getFriendList(request.user)
		blockList=getBlockList(request.user)
		blockList.append(request.user)
		# is friend not myself
		grumblrList=list(Grumblr.objects.filter(owner__in=friendList).exclude(owner__in=blockList).order_by('-publishDateTime')[:5])


	context=getUserStatistics(request.user)

	recommendFriendList=getRecommendFriendList(request,request.user)
	context['recommendFriendList']=recommendFriendList

	context['user']=request.user
	context['grumblrList']=grumblrList
	return render_to_response('home.html',context,context_instance=RequestContext(request))

def postGrumblr(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/login')

	if request.POST:
		content=request.POST['content']
		user=request.user
		currentTime=datetime.datetime.now()
		grumblr=Grumblr(content=content,owner=user,publishDateTime=currentTime)
		grumblr.save();

		# save image later in order to get grumblr id
		if request.FILES.get('grumblrImage'):
			image=request.FILES['grumblrImage']
			grumblr.image=image
			grumblr.save()

	return HttpResponseRedirect("/home")

def postGrumblrComment(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/login')

	if request.POST:
		form=GrumblrCommentForm(request.POST)
		if form.is_valid():
			user=request.user
			currentTime=datetime.datetime.now()
			comment=request.POST['comment']
			grumblrId=request.POST['grumblrId']
			grumblr=Grumblr.objects.get(id=grumblrId)

			comment=GrumblrComment(owner=user,grumblr=grumblr,comment=comment,publishDateTime=currentTime)
			comment.save()

			context={}
			context['errors']=form.errors

		return HttpResponse(json.dumps(form.errors), content_type="application/json")

	return HttpResponse(json.dumps({}), content_type="application/json")

def getGrumblrComment(request):

	if request.POST:
		context={};
		authorList=[];
		contentList=[];

		grumblrId=request.POST['grumblrId']
		comments=GrumblrComment.objects.filter(grumblr=grumblrId).order_by('-publishDateTime')[:5]

		for comment in comments:
			# owner=User.objects.get(id=comment.owner)
			authorList.append(comment.owner.username)
			contentList.append(comment.comment)

		context['authorList']=authorList
		context['contentList']=contentList
		return HttpResponse(json.dumps(context), content_type="application/json")

	return HttpResponse(json.dumps({}), content_type="application/json")


def logout(request):
	if request.user.is_authenticated():
		auth.logout(request)
	return HttpResponseRedirect("/")

def searchGrumblr(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/login')

	context=getUserStatistics(request.user)
	recommendFriendList=getRecommendFriendList(request,request.user)
	context['recommendFriendList']=recommendFriendList
	context['user']=request.user

	if request.GET:
		keyWord=request.GET['keyWord']

		friendList=getFriendList(request.user)
		friendList.append(request.user)
		blockList=getBlockList(request.user)
		# is friend not block
		grumblrList=list(Grumblr.objects.filter(owner__in=friendList).exclude(owner__in=blockList).order_by('-publishDateTime')[:5])

		resultList=[];

		for grumblr in grumblrList:
			if keyWord in grumblr.content:
				resultList.append(grumblr)

		context['grumblrList']=resultList

	return render_to_response('home.html',context,context_instance=RequestContext(request))



def getSelfAvatar(request):
	if not request.user.avatar:
		raise Http404

	contentType=guess_type(request.user.avatar.name)
	return HttpResponse(request.user.avatar, mimetype=contentType)

def getAvatar(request, id):
	user=User.objects.get(username=id)
	#print(user.avatar)
	if  len(user.avatar.name)==0:

		#default image
		#print abspath(dirname(__file__))
		default=Image.open("/media/avatar/default.jpg")
		content_type = guess_type(path)
		#print(path)
		return HttpResponse(path, mimetype=content_type)
	else:
		content_type = guess_type(user.avatar.name)
		return HttpResponse(user.avatar, mimetype=content_type)

def getGrumblrImage(request, id):
	grumblr=Grumblr.objects.get(id=id)
	if len(grumblr.image.name)>0:
		content_type = guess_type(grumblr.image.name)
		return HttpResponse(grumblr.image, mimetype=content_type)

def personalPage(request, id):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/login')

	user=User.objects.get(username=id)
	grumblrList=list(Grumblr.objects.filter(Q(owner=user)).order_by('-publishDateTime')[:5])

	context=getUserStatistics(user)
	context['grumblrList']=grumblrList
	context['user']=user

	isFriend=MyUserFriend.objects.filter(user=request.user, friend=user)
	isBlock=MyUserBlock.objects.filter(user=request.user, block=user)

	if isBlock:
		context['isBlock']=True
	else:
		context['isBlock']=False

	if isFriend:
		context['isFriend']=True
	else:
		context['isFriend']=False

	if user.username==request.user.username:
		context['isSelf']=True
	else:
		context['isSelf']=False

	return render_to_response('personalPage.html',context,context_instance=RequestContext(request))

def followFriend(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/login')

	if request.POST:
		friendName=request.POST['friendName']
		friend=User.objects.get(username=friendName)
		if friend:
			tempRelationship = MyUserFriend.objects.filter(user=request.user,friend=friend)
			# not exist friend relationship then add
			if not tempRelationship:
				relationship=MyUserFriend(user=request.user,friend=friend)
				relationship.save()
			return personalPage(request, friendName)

	return personalPage(request, request.user.username)


def deFollowFriend(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/login')

	if request.POST:
		friendName=request.POST['friendName']
		friend=User.objects.get(username=friendName)

		if friend:
			relationship=MyUserFriend.objects.get(user=request.user,friend=friend)
			relationship.delete()
			return personalPage(request, friendName)

	return personalPage(request, request.user.username)

def blockUser(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/login')

	if request.POST:
		friendName=request.POST['friendName']
		friend=User.objects.get(username=friendName)
		if friend:
			relationship=MyUserBlock(user=request.user,block=friend)
			relationship.save()
			return personalPage(request, friendName)

	return personalPage(request, request.user.username)

def deBlockUser(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/login')

	if request.POST:
		friendName=request.POST['friendName']
		friend=User.objects.get(username=friendName)

		print(friend)
		if friend:
			relationship=MyUserBlock.objects.get(user=request.user,block=friend)
			relationship.delete()
			return personalPage(request, friendName)

	return personalPage(request, request.user.username)


def thumbUpGrumblr(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/login')

	if request.POST:
		grumblrId=request.POST['grumblrId']
		grumblr=Grumblr.objects.get(id=grumblrId)
		hasThumbUp=GrumblrThumbUp.objects.filter(grumblr=grumblr, owner=request.user)
		if not hasThumbUp:
			thumbUp=GrumblrThumbUp(grumblr=grumblr,owner=request.user)
			thumbUp.save()
			grumblr.thumbUp=grumblr.thumbUp+1
			grumblr.save()


	return HttpResponseRedirect("/home")



def getUserRelationships(user, type):
	nameList=[]
	if type=='Followers':
		informations=MyUserFriend.objects.filter(friend=user)
		for temp in informations:
			nameList.append(temp.user.username)
	elif type=='Followings':
		informations=MyUserFriend.objects.filter(user=user)
		for temp in informations:
			nameList.append(temp.friend.username)
	elif type=='Blocks':
		informations=MyUserBlock.objects.filter(user=user)
		for temp in informations:
			nameList.append(temp.block.username)
	elif type=='Grumblrs':
		informations=Grumblr.objects.filter(owner=user)
		for temp in informations:
			nameList.append(temp.owner.username)
	return nameList


def getUserStatistics(user):
	statistics={};
	statistics["Followers"]=len(getUserRelationships(user,"Followers"))
	statistics["Followings"]=len(getUserRelationships(user,"Followings"))
	statistics["Blocks"]=len(getUserRelationships(user,"Blocks"))
	statistics["Grumblrs"]=len(getUserRelationships(user,"Grumblrs"))
	return statistics

def getFriendList(user):
	friendList=[]
	for friendRelationship in MyUserFriend.objects.filter(user=user):
		friendList.append(friendRelationship.friend)
	return friendList

def getBlockList(user):
	blockList=[]
	for blockRelationship in MyUserBlock.objects.filter(user=user):
		blockList.append(blockRelationship.block)
	return blockList

def getRecommendFriendList(request, user):
	friendList=getFriendList(user)
	friendList.append(request.user)
	# not friend and myself
	friendNameList=[]
	for friend in friendList:
		friendNameList.append(friend.username)

	print(friendNameList)
	print(request.user)

	recommendFriendList=[]
	for recommend in User.objects.exclude(username__in=friendNameList).order_by('?')[:2]:
		recommendFriendList.append(recommend)

	print(recommendFriendList)
	return recommendFriendList

def refreshGrumblrList(request):
	context={}
	if request.POST:
		grumblrPublishTime=[]

		latestGrumblrTime=request.POST['latestGrumblrTime']

		friendList=getFriendList(request.user)
		friendList.append(request.user)
		blockList=getBlockList(request.user)

		#no time then give default value
		if latestGrumblrTime:
			d1=datetime.datetime.strptime(latestGrumblrTime,"%d-%m-%Y %H:%M:%S")
		else:
			d1=d1=datetime.datetime.strptime("01-01-1900 18:00:00","%d-%m-%Y %H:%M:%S")

		d2=datetime.datetime.now()
		newGrumblrList=list(Grumblr.objects.filter(owner__in=friendList).filter(publishDateTime__range=(d1,d2)).exclude(owner__in=blockList).order_by('-publishDateTime'))

		if len(newGrumblrList)>0:
			grumblrList=list(Grumblr.objects.filter(owner__in=friendList).exclude(owner__in=blockList).order_by('-publishDateTime')[:5])
			context['haveNewGrumblrs']=True
			context['grumblrList']=grumblrList
		else:
			context['haveNewGrumblrs']=False
			context['grumblrList']=grumblrList

	return HttpResponse(json.dumps(context,cls=GrumblrEncoder), content_type="application/json")

def changePassword(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/login')


	if request.method=="POST":
		form=ChangePasswordForm(request.user,request.POST)
		if form.is_valid():
			request.user.set_password(request.POST['newPassword']);
			request.user.save();

		return HttpResponse(json.dumps(form.errors), content_type="application/json")

	else:
		context=getUserStatistics(request.user)
		context['user']=request.user
		context['form']=ProfileForm()



		recommendFriendList=getRecommendFriendList(request,request.user)
		context['recommendFriendList']=recommendFriendList


		return render_to_response('changePassword.html',context,context_instance=RequestContext(request))


def findPassword(request):
	context={}

	if request.method=='POST':
		userName= request.POST.get("userName")
		user = User.objects.get(username=userName)
		if user:
			email=user.email
			newPassword=''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(6))
			print newPassword
			user.set_password(newPassword)
			user.save()
			send_mail('Password Reset','Your password has been reseted to '+newPassword+'. Please login the system and revise your password immediately.','mengyanw@andrew.cmu.edu',[email],fail_silently=False)
			context['reset']=True;


	return render_to_response('findPassword.html',context,context_instance=RequestContext(request))