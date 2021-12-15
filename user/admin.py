from django import forms
from django.contrib import admin
from django.contrib.auth import models
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from management.models import Car

from .models import User


class CarInline(admin.StackedInline):
    model = Car
    extra = 1

class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
    national_code = forms.IntegerField(max_value=10 ** 10, min_value=1000)
    age = forms.IntegerField(min_value=1)

    class Meta:
        model = User
        fields = ('name', 'national_code', 'age', 'total_toll_paid')

    def clean_password2(self):

        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):

        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """
    password = ReadOnlyPasswordHashField()
    national_code = forms.IntegerField(max_value=10 ** 10, min_value=1000)
    age = forms.IntegerField(min_value=1)

    class Meta:
        model = User
        fields = ('name', 'national_code', 'age','total_toll_paid', 'password', 'is_active', 'is_admin')


class UserAdmin(BaseUserAdmin):

    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('name', 'is_admin', 'national_code')
    list_filter = ('is_admin','national_code',)
    fieldsets = (
        (None, {'fields': ('name', 'password')}),
        ('Personal info', {'fields': ('national_code', 'age','total_toll_paid',)}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'national_code', 'age','total_toll_paid', 'password1', 'password2'),
        }),
    )
    search_fields = ('name','national_code',)
    ordering = ('name',)
    filter_horizontal = ()

    inlines = [CarInline]


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)