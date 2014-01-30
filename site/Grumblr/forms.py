from django import forms
from Grumblr.models import Grumblr

class GrumblrForm(forms.Form):
	content=forms.CharField(max_length=100, error_messages={'required':'Please type something:-)'});

class GrumblrCommentForm(forms.Form):
	grumblrId=forms.CharField(max_length=50, error_messages={'required':'Please type something:-)'});
	comment=forms.CharField(max_length=50, error_messages={'required':'Please type something:-)'});

	def clean_grumblrId(self):
		grumblrId=self.cleaned_data['grumblrId']
		if len(Grumblr.objects.filter(id=grumblrId))<=0:
			raise forms.ValidationError('Grumblr does not exist')
		return grumblrId

