from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

from blog.models import Post

# Create your models here.


class AccountManager(BaseUserManager):
    def create_user(self, email, user_name, password=None, **other_fields):
        if not email:
            raise ValueError("You must provide an email address")
        if not user_name:
            raise ValueError("You must provide a username")
        
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            user_name=user_name,
            **other_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, user_name, password=None, **other_fields):
        other_fields.setdefault("is_staff", True)
        other_fields.setdefault("is_superuser", True)
        other_fields.setdefault("is_active", True)

        if other_fields.get("is_staff") is not True:
            raise ValueError("Superuser must be assigned to is_staff=True.")
        if other_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must be assigned to is_superuser=True.")
        
        user =  self.create_user(email, user_name, password=password, **other_fields)
        user.save(using=self._db)
        return user

        
    

class Account(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField("email address", unique=True)
    user_name = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(auto_now=True)
    about = models.TextField(max_length=500, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False) 

    objects = AccountManager()

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = ["user_name",]

    def __str__(self):
        return self.user_name
    
    def post_count(self):
        return self.blog_posts.filter(status="published").count()


class UserProfile(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to="profile", default="profile/profile.png")
    address = models.CharField(max_length=250, blank=True)
    date_completed = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.user_name} - {self.date_completed}"