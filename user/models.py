from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.db.models import constraints
from django.db.models.base import Model
from . import validators
from django.db.models import Count
from django.db.models import constraints


class MyUserManager(BaseUserManager):
    def create_user(self, name, national_code, age, total_toll_paid, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if national_code < 10000 or national_code > 10 ** 10:
            raise ValueError('National Code is too long or too small')
        if age < 18:
            raise ValueError('Age must be an integer greater than 18')

        user = self.model(
            name=name,
            national_code=national_code,
            age=age,
            total_toll_paid=total_toll_paid
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name, national_code, age, total_toll_paid, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            name=name,
            national_code=national_code,
            age=age,
            total_toll_paid=total_toll_paid,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    name = models.CharField(
        verbose_name='name',
        max_length=255
    )
    national_code = models.PositiveBigIntegerField(
        unique=True, validators=[validators.validate_national_code]
    )
    age = models.PositiveSmallIntegerField(validators=[validators.validate_age])
    total_toll_paid = models.PositiveBigIntegerField()
    REQUIRED_FIELDS = ['name', 'age', 'total_toll_paid']
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'national_code'

    def __str__(self):
        return self.name

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    def ser():
        return True

    # class Meta:
    #     constraints = [
    #         constraints.CheckConstraint(
    #             check=Model() .objects.filter(national_code=8569875425,cars__type='big').
    #                 values('id').annotate(xx=Count('id')).filter(xx__lt=1),
    #             name='Check only one car exist with big type'
    #         )
    #     ]


