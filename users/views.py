import os
import requests
from users import models
from django.contrib import auth
from django.http.response import HttpResponseRedirectBase
from django.views import View
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.shortcuts import render,redirect,reverse
from django.contrib.auth import authenticate,login,logout
from . import forms

# Create your views here.
'''
class LoginView(View):

    def get(self,request):
        form = forms.LoginForm()
        return render(request,"users/login.html",{"form":form})

    def post(self,request):
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(request,username=email,password=password)
            if user is not None:
                login(request,user)
                return redirect(reverse("core:event"))

        return render(request,"users/login.html",{"form":form})
'''

# implementing using form view

class LoginView(FormView):
    
    template_name = "users/login.html"
    form_class = forms.LoginForm
    success_url = reverse_lazy("core:event")

    def form_valid(self,form):
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(self.request,username=email,password=password)
            if user is not None:
                login(self.request,user)
                return super().form_valid(form)


def log_out(request):
    logout(request)
    return redirect(reverse("core:event"))
 
 
class SignUpView(FormView):
    
    template_name = "users/signup.html"
    form_class = forms.SignUpForm
    success_url = reverse_lazy("core:event")

    def form_valid(self,form):
        form.save()
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request,username=email,password=password)
        if user is not None:
            login(self.request,user)
        
        user.verify_email()
        return super().form_valid(form)
    
def complete_verification(request,key):
    try:
        user = models.User.objects.get(email_secret=key)
        user.email_verified = True
        user.email_secret = ""
        user.save()
        # success message here
    except models.User.DoesNotExist:
        # failed message here
        pass

    return redirect(reverse("core:event"))


def github_login(self):
    client_id = os.environ.get("GITHUB_ID")
    redirect_uri = "http://127.0.0.1:8000/users/login/github/callback"
    return redirect(f"https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope=read:user,user:email")

class GithubException(Exception):
    pass

def github_callback(request):
    try:
        client_id = os.environ.get("GITHUB_ID")
        client_secret = os.environ.get("GITHUB_SECRET")
        code = request.GET.get("code","None")
        if code is not None:
            token_request = requests.post(
                f"https://github.com/login/oauth/access_token?client_id={client_id}&client_secret={client_secret}&code={code}",
                headers={"Accept": "application/json"},
            )
            result_json = token_request.json()
            error = result_json.get("error",None)
            if error is not None:
                return GithubException("Can't get the access token")
            else:
                access_token = result_json.get("access_token")
                profile_request = requests.get(
                    "https://api.github.com/user",
                    headers={
                        "Authorization": f"token {access_token}",
                        "Accept": "application/json",
                    },
                )
                email_request = requests.get(
                    "https://api.github.com/user/emails",
                    headers={
                        "Authorization": f"token {access_token}",
                        "Accept": "application/json",
                    },
                )
                email_json = email_request.json()
                profile_json = profile_request.json()
                print(profile_json)
                username = profile_json.get("login",None)
                if username is not None:
                    name = profile_json.get("name")
                    email = email_json[0].get("email")
                    # user = models.User.objects.get(email=email)
                    try:
                        user = models.User.objects.get(email=email)
                        if user.login_method != models.User.LOGIN_GITHUB:
                            raise GithubException (
                                f"Please login with:{user.login_method}"
                            )
                    except models.User.DoesNotExist:
                        user = models.User.objects.create(username=email,first_name=name,email=email,login_method = models.User.LOGIN_GITHUB,email_verified=True,)
                        user.set_unusable_password()
                        user.save()
                    login(request,user)
                    return redirect(reverse("core:event"))

                    
                    # if user is not None:
                    #     return redirect(reverse("users:login"))
                    # else:
                    #     user = models.User.objects.create(username=email,first_name=name,email=email)
                    #     login(request,user)
                    #     return redirect(reverse("core:event"))
                else:
                    raise GithubException("Can't get your profile")
        else:
            raise GithubException("Can't get code")
    except GithubException as err:
        print(err)
        return redirect(reverse("users:login"))