from django.db import models
from UserProfile.models import MyUser
import json
import os



def generate_new_filename(instance, filename):
    ext = filename.split('.')[-1]
    fileName="%s.%s" %(str(instance.id),ext)
    print instance.id
    print instance.content
    print 111111

    return os.path.join('GrumblrImage', fileName)

class Grumblr(models.Model):
	content=models.CharField(max_length=200)
	owner=models.ForeignKey(MyUser)
	publishDateTime=models.DateTimeField()
	thumbUp=models.PositiveIntegerField(default=0)
	image=models.ImageField(blank=True, upload_to=generate_new_filename)
	# def __init__(self, content, owner, publishDateTime, thumbUp=0):
	# 	self.content=content
	# 	self.owner=owner
	# 	self.publishDateTime=publishDateTime
	# 	self.publishDateTime=self.publishDateTime.strftime("%d-%m-%Y %H:%M:%S")
	# 	self.thumbUp=thumbUp

class GrumblrEncoder(json.JSONEncoder):
	def default(self, obj):
		dic={}
		try:
			if isinstance(obj, Grumblr):
				dic['id']=obj.id
				dic['content']=obj.content
				dic['owner']=str(obj.owner)
				dic['publishDateTime']=obj.publishDateTime.strftime("%d-%m-%Y %H:%M:%S")
				dic['thumbUp']=obj.thumbUp
				dic['image']=str(obj.image).split("/")[-1].split(".")[0];
				print dic
				return dic
			else:
				print 123123123
		except Exception, e:
			print str(e)

class GrumblrComment(models.Model):
	owner=models.ForeignKey(MyUser)
	grumblr=models.ForeignKey(Grumblr)
	comment=models.CharField(max_length=200)
	publishDateTime=models.DateTimeField()

class GrumblrThumbUp(models.Model):
	owner=models.ForeignKey(MyUser)
	grumblr=models.ForeignKey(Grumblr)


