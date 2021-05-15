import uuid
from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.template.loader import render_to_string
# Create your models here.
class User(AbstractUser):

    '''Custom User model'''

    GENDER_MALE = "male"
    GENDER_FEMALE = "female"
    GENDER_OTHER = "other"

    GENDER_CHOICES = (
        (GENDER_MALE, "Male"),
        (GENDER_FEMALE,"Female"),
        (GENDER_OTHER,"Other")
    )

    LOGIN_EMAIL = "email"
    LOGIN_GOOGLE = "google"
    LOGIN_GITHUB = "github"

    LOGIN_CHOICES = (
        (LOGIN_EMAIL,"Email"),
        (LOGIN_GOOGLE,"Google"),
        (LOGIN_GITHUB,"Github"),
    )

    avatar = models.ImageField(upload_to = "avatars",blank = True)
    gender = models.CharField(choices=GENDER_CHOICES,max_length=10,blank=True)
    bio = models.TextField(blank=True)
    superorganizer = models.BooleanField(default = False)

    email_verified = models.BooleanField(default=False)
    email_secret = models.CharField(max_length=30,default="",blank=True)
    login_method = models.CharField(max_length=50,choices=LOGIN_CHOICES,default=LOGIN_EMAIL)
    def verify_email(self):
        if self.email_verified is False:
            secret = uuid.uuid4().hex[:30]
            self.email_secret = secret
            html_message = render_to_string("emails/verify_email.html",{"secret":secret})
            send_mail(
                "Verify your Eventhub Account",
                strip_tags(html_message),
                settings.EMAIL_FROM,
                [self.email],
                fail_silently=False,
                html_message=html_message,
                )
            self.save()
        return