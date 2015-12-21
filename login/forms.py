
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

class MyRegistrationForm(UserCreationForm) :
	alphabetic = RegexValidator(r'^[a-zA-Z]*$', 'Only alphabetic characters are allowed.')
	username = forms.CharField(max_length=20, required=True, widget=forms.TextInput(attrs={ 'required': 'true' }))
	email = forms.EmailField(required = True, widget=forms.TextInput(attrs={ 'required': 'true' }))
	first_name = forms.CharField(max_length=20, required=True, widget=forms.TextInput(attrs={ 'required': 'true' }),validators=[alphabetic])
	last_name = forms.CharField(max_length=20, required=True, widget=forms.TextInput(attrs={ 'required': 'true' }),validators=[alphabetic])
	
	class Meta:
		model = User
		fields = ('username','first_name' ,'last_name','email' , 'password1' , 'password2')

	def save(self , commit= True):
		user = super(MyRegistrationForm, self).save(commit= False)	
		user.first_name = self.cleaned_data['first_name']
		self.fields['username'].required = True
		self.fields['first_name'].required = True
		self.fields['last_name'].required = True
		self.fields['email'].required = True
		user.last_name = self.cleaned_data['last_name']
		if commit:
			user.save()
		return user

class GuessForm(forms.Form):
	def __init__(self, *args, **kwargs):
		num_choices = kwargs.pop('num_choices')
		super(GuessForm, self).__init__(*args, **kwargs)
		self.fields['choice'] = forms.TypedChoiceField(coerce=int,widget=forms.TextInput,choices=[(str(x), str(x)) for x in xrange
			(num_choices)],error_messages={'required': 'Please select a number from 1 to 5'})
