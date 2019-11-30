from django.contrib.auth.models import User
from django import forms
from .models import Profile

class UserForm(forms.ModelForm):
	password = forms.CharField(widget= forms.PasswordInput)
	confirm_password = forms.CharField(widget= forms.PasswordInput)
	full_name = forms.CharField(required= True)
	codeforces_id = forms.CharField(required= True)
	Uva_Id = forms.CharField(required= True)
	department = forms.CharField(required= True)

	class Meta:
		model = User
		fields=('username','email','password','full_name','codeforces_id','Uva_Id','department')

	def clean(self):
		cleaned_data= super(UserForm,self).clean()
		password=  cleaned_data.get("password")
		confirm_password= cleaned_data.get("confirm_password")
		if password != confirm_password:
			raise forms.ValidationError(
				"password doesn't match!"
			)
