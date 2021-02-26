from django.contrib import admin
from django.contrib.auth.models import Permission
from .models import User, Country, LeaveRequest


# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'name', 'birth_date', 'image')

    def name(self, obj):
        return obj.get_full_name()


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name_ar', 'name_en', 'logo')


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'codename')


@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ('reason', 'user')
