from django.contrib import admin
from .models import User, Board

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



class BoardAdmin(admin.ModelAdmin):
    list_display = ('title', 'writer', 'created_at', 'updated_at')

admin.site.register(Board, BoardAdmin)




# class NoticeAdmin(admin.ModelAdmin):
#     list_display = (
#         'title', 
#         'writer', 
#         'hits',
#         'registered_date',
#         )
#     search_fields = ('title', 'content', 'writer__user_id',)

# admin.site.register(Notice, NoticeAdmin)