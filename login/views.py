
from django.shortcuts import render_to_response, render
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from django.contrib import auth
from random import randint
from django.http import HttpResponse
from forms import MyRegistrationForm
from forms import GuessForm
from django.contrib.auth.models import User
from django.template import RequestContext, loader
from django.shortcuts import get_object_or_404, render ,redirect
from django.core.urlresolvers import reverse
from datetime import datetime 
from django.utils import timezone



def index(request):
    return render_to_response('homepage.html', context_instance=RequestContext(request))

def login(request):
	c= {}
	c.update(csrf(request))
	t = loader.get_template('login.html')
	r = RequestContext(request, { } )
	return HttpResponse(t.render(r), content_type=c)


def auth_view(request):
	if request.method == 'POST':
		username = request.POST.get('username' , '')
		password = request.POST.get('password' , '')
		user = auth.authenticate(username=username , password = password)
		if "username" not in request.session or (username == request.session["username"]) :
			if user is not None :
				auth.login(request, user)
				request.session["username"] = username
				return HttpResponseRedirect('/accounts/loggedin/')
			else :
				return HttpResponseRedirect('/accounts/invalid/')
		else :
			return HttpResponse("user already logged in")
		
		

def invalied_login(request):
	return render_to_response('invalied_login.html')


def loggedin(request):
	if request.user.id is not None :
		try:
			return render_to_response('loggedin.html' , {'full_name' : request.user.username })
		except :
			return render_to_response('loggedin.html' , {'full_name' : request.user.username })
	else :
		return login(request)


def logout(request):
	auth.logout(request)
	if "username" in request.session:
		del request.session["username"]
	return render_to_response('logout.html')

def register_user(request):
	if request.method == 'POST' :
		form = MyRegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/accounts/register_sucesss/')
		else:
			return render_to_response('registerpasswordsmatch_alert.html')
			
	args = {}
	args.update(csrf(request))
	args['form'] = MyRegistrationForm()
	return render_to_response('register.html' ,args)

def register_sucesss(request):
	return render_to_response('register_sucesss.html')

def game(request):
	return render_to_response('game.html')

def start_game(request):
	request.session[ATTEMPT_COUNTER] = None
	request.session[NUMBER_TO_GUESS] = randint(0, NUM_CHOICES - 1)
	request.session[ATTEMPT_COUNTER] = 1
	return redirect('/accounts/play')

ATTEMPT_COUNTER = 'ATTEMPT_COUNTER'
NUMBER_TO_GUESS = 'NUMBER_TO_GUESS' 
NUM_CHOICES = 6

def play(request):
	form = GuessForm(request.POST, num_choices = NUM_CHOICES) if request.POST else GuessForm(num_choices = NUM_CHOICES)
	attempts = int(request.session[ATTEMPT_COUNTER])
	request.session[ATTEMPT_COUNTER] = int(request.session[ATTEMPT_COUNTER]) + 1
	if form.is_valid():
		number_to_guess = int(request.session[NUMBER_TO_GUESS])
		guess = form.cleaned_data['choice']

		if guess == number_to_guess:
			return redirect('/accounts/success')
		elif attempts > 3:
			return render(request, 'fail.html')
		else:
			return render(request, 'game.html',{'form' : form})

	return render(request, 'game.html',{'form' : form})

def success(request):
	attempts = int(request.session[ATTEMPT_COUNTER])
	number_guess = int(request.session[NUMBER_TO_GUESS])
	message = ''
	if attempts > 3:
		message = 'You must try in three attempts! and correct number is %d' %number_guess
		return render(request, 'fail.html', {'message' : message})
	else:
		return render(request, 'success.html',)