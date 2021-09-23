from django.contrib import admin
from .models import User

from django import forms
# Register your models here.

# admin.site.register(User)
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'userid',
        'username',
        'useremail',
        'phoneNumber',
        'registered'
    )

    list_display_links = (
        'userid',
        'username',
        'phoneNumber',
        'registered'
    )