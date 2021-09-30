from django import forms
from .models import Board

# from ckeditor.fields import RichTextFormField
# from ckeditor_uploader.fields import RichTextUploadingFormField

# class CkEditorForm(forms.Form):
#     ckeditor_standard_example = RichTextFormField()
#     ckeditor_upload_example = RichTextUploadingFormField(
#         config_name = "my-custom-toolbar"
#     )

# class CommentForm(forms.Form):
#     name = forms.CharField(label='Your name')
#     url = forms.URLField(label='Your website', required=False)
#     comment = forms.CharField()

# Your name : <input type="text" name="name" required>
# Your website : <input type="url" name="url">

class BoardForm(forms.Form):
    title = forms.CharField(error_messages = {'required' : '제목을 입력하세요.'},
                            max_length=100,
                            label = '게시글 제목')
    contents = forms.CharField(error_messages = {'required' : '내용을 입력하세요.'},
                                widget = forms.Textarea,
                                label = '게시글 내용')