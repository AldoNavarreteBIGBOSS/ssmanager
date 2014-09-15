from django.shortcuts import redirect, render 
from myapp.modulos.presentacion.forms import RegisterForm, LoginForm, RecoverPasswordForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from myapp.modulos.principal.models import userProfile
from google.appengine.api import mail
from django.core.mail import send_mail

# Create your views here.
def welcome_view(request):
	return render(request, 'presentacion/welcome.html')

def tour_view(request):
	return render(request,'presentacion/tour.html')

def method_view(request):
	return render(request,'presentacion/method.html')

def about_view(request):
	return render(request,'presentacion/about.html')

def signup_view(request):
	
	form = RegisterForm()
	if request.method == "POST":
		form = RegisterForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			name = form.cleaned_data['name']
			last_name = form.cleaned_data['last_name']
			email = form.cleaned_data['email']
			password_one = form.cleaned_data['password_one']
			password_two = form.cleaned_data['password_two']
			newUser = User.objects.create_user(username=username, first_name=name, last_name=last_name, email=email, password=password_one)
			newUserProfile = userProfile.objects.create(user=newUser)
			newUser.save()
			newUserProfile.save()

			return redirect('/login')
		else:
			ctx = {'form':form}
			return render(request,'presentacion/sign_up.html',ctx)
	ctx = {'form':form}
	return render(request,'presentacion/sign_up.html',ctx)

def login_view(request):

	status = ""
	if request.user.is_authenticated():
		return redirect('/') #Cambiar cuando este el estado disponible
	else:
		if request.method == "POST":
			form = LoginForm(request.POST)
			if form.is_valid():
				username = form.cleaned_data['username']
				password = form.cleaned_data['password']
				user = authenticate(username=username, password=password)
				if user is not None and user.is_active:
					login(request, user)
					return redirect('vista_principal')
				else:
					status = "Usuario y/o Password incorrecto"
		form = LoginForm()
		ctx = {'form':form, 'status': status}
		return render(request,'presentacion/login.html',ctx)

	return render(request,'presentacion/login.html')

def logout_view(request):
	logout(request)
	return redirect('/')

def recover_view(request):
 	form = RecoverPasswordForm()
 	status=""
 	if request.method == "POST":
 		form = RecoverPasswordForm(request.POST)
 		if form.is_valid():
 			message = mail.EmailMessage(sender="Aldo Navarrete <arden.papifunk@gmail.com>",
 				subject="Your account has been approved")

 			message.to = "Aldo Navarrete <aldo.navarrete@usach.cl>"
 			message.body = """
 			Dear Albert:

 			Your example.com account has been approved.  You can now visit
 			http://www.example.com/ and sign in using your Google Account to
 			access new features.

 			Please let us know if you have any questions.

 			The example.com Team
 			"""

 			message.send()
			
 			#send_mail('test email', 'hello world', 'arden.papifun@gmail.com', ['aldo.navarrete@usach.cl'])

 			status="Correo enviado"
 			form = RecoverPasswordForm()
 			ctx={'status' : status, 'form' : form}
 			return render(request, 'presentacion/recover_password.html', ctx)

 	ctx={'form' : form}
	return render(request, 'presentacion/recover_password.html', ctx)

