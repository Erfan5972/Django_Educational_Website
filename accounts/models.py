from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .manager import UserManager


class User(AbstractBaseUser):
    phone_number = models.CharField(max_length=11, unique=True)
    full_name = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["full_name"]

    objects = UserManager()

    def __str__(self):
        return f"{self.phone_number} - {self.full_name}"

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class UserOtpCode(models.Model):
    code = models.CharField(max_length=4)
    phone_number = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.code}'


class Subscription(models.Model):
    count = models.IntegerField()
    price = models.BigIntegerField()

    def __str__(self):
        return f'count : {self.count} - price: {self.price}'


class UserSubscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_subscription')
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, related_name='subscription_user')