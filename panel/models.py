from django.db import models
from django.core.validators import MinLengthValidator, RegexValidator
from phonenumber_field.modelfields import PhoneNumberField
from django.conf import settings


# Create your models here.

class Invoice(models.Model):
    name = models.CharField(
        max_length=60,
        validators=[MinLengthValidator(3, " must be greater than 3 character")]
        )
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


    def __str__(self):
        return self.name


class People(models.Model):
    name = models.CharField(
        max_length=60,
        validators=[MinLengthValidator(4, " must be greater than 4 character")]
        )
    username = models.CharField(
        max_length=60,
        validators=[MinLengthValidator(4, " must be greater than 4 character")],
        unique=True,
        null=True,
        blank=True
        )
    active = models.BooleanField(default=True)
    invoice = models.ForeignKey(Invoice,on_delete=models.CASCADE)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,11}$', message="Phone number must be entered in the format: '0912*******'. Up to 11 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=11, blank=True) # validators should be a list
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    
    def __str__(self):
        return self.name


class Transaction(models.Model):
    name = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(4, " must be greater than 4 character")]
        )
    price = models.DecimalField(max_digits=9, decimal_places=0)
    payer = models.ForeignKey(People, null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    invoice = models.ForeignKey(Invoice,on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    persons = models.ManyToManyField(People, related_name="action_persons")


    def __str__(self):
        return self.name