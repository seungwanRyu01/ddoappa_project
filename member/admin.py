from django.contrib import admin
from .models import User, Board
from django_summernote.admin import SummernoteModelAdmin
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


@admin.register(Board)
class BoardAdmin(SummernoteModelAdmin):
    summernote_fields = ('contents',)
    list_display = (
        'title',
        'contents',
        'writer',
        'board_name',
        'hits',
        'write_dttm',
        'update_dttm'
    )
    list_display_links = list_display




# class NoticeAdmin(admin.ModelAdmin):
#     list_display = (
#         'title', 
#         'writer', 
#         'hits',
#         'registered_date',
#         )
#     search_fields = ('title', 'content', 'writer__user_id',)

# admin.site.register(Notice, NoticeAdmin)