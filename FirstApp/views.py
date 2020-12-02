from django.shortcuts import render
from django.core.mail import send_mail
from ForgotPwd import settings
import random
from django.http import HttpResponse
from FirstApp.models import Student

# Create your views here.
def register(req):
	if req.method=="POST":
		fname=req.POST["fname"]
		lname=req.POST["lname"]
		clgname=req.POST["clgname"]
		email=req.POST["email"]
		password=str(random.randint(1000,100000))+lname[1:]
		Student.objects.create(firstname=fname,lastname=lname,email=email,collegename=clgname,password=password)

		sender=settings.EMAIL_HOST_USER
		receiver=email
		subject="Reg. Registration details"
		body="Hello {}\n\n This is your username {}\n\n Your password is {}".format(fname,email,password)
		send_mail(subject,body,sender,[receiver])
		return HttpResponse("<h1>Done!!!</h1>")
	return render(req,'app/register.html')

def login(req):
	if req.method=="POST":
		uname=req.POST['username']
		pwd=req.POST['password']
		data=Student.objects.all().filter(email=uname,password=pwd)
		if data:
			return HttpResponse("<h1>Welcome {} {}</h1>".format(data[0].firstname,data[0].lastname))
		else:
			return HttpResponse("No account with that email!!")
	return render(req,"app/login.html")

def forgot(req):
	if req.method=='POST':
		email=req.POST['email']
		data=Student.objects.get(email=email)
		sender=settings.EMAIL_HOST_USER
		receiver=email
		subject="Reg. Password Info"
		body="Your password is "+data.password
		send_mail(subject,body,sender,[receiver])
		if data:
			return HttpResponse("<h1>Check your mail for your password</h1>")
		else:
			return HttpResponse("No account with email!!")


	return render(req,'app/forgot.html')