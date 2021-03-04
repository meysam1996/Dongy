from django.db import models
from django.core.validators import MinLengthValidator, RegexValidator
from phonenumber_field.modelfields import PhoneNumberField
from django.conf import settings


# Create your models here.

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
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,11}$', message="Phone number must be entered in the format: '0912*******'. Up to 11 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=11, blank=True) # validators should be a list
    

    def __str__(self):
        return "%s : %s => %s" % (self.name, self.phone_number, self.active)


class Transaction(models.Model):
    name = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(4, " must be greater than 4 character")]
        )
    price = models.DecimalField(max_digits=9, decimal_places=0)
    payer = models.ForeignKey(People, null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Transaction_name: %s => Price: %s => Payer: %s" % (self.name, self.price, self.payer)


class Invoice(models.Model):
    name = models.CharField(
        max_length=60,
        validators=[MinLengthValidator(3, " must be greater than 3 character")]
        )
    people = models.ManyToManyField(People)
    transaction = models.ManyToManyField(Transaction)

    @property
    def people_num(self):
        return self.people.all().count()


    def __str__(self):
        return self.name