from django import contrib, forms
from django.forms import widgets
from .models import Board
from django import forms
from django_summernote.fields import SummernoteTextField
from django_summernote.widgets import SummernoteWidget

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

class BoardWriteForm(forms.ModelForm):
    title = forms.CharField(
        label='글 제목',
        widget = forms.TextInput(
            attrs = {
                'placeholder' : '게시글 제목'
            }),
        required=True,
    )

    contents = SummernoteTextField()

    options = (
        ('Consulting Record', '상담 게시판'),
        ('notice', '공지사항')
    )

    board_name = forms.ChoiceField(
        label = '게시판 선택',
        widget = forms.Select(),
        choices = options
    )

    field_order = [
        'title',
        'board_name',
        'contents'
    ]


    class Meta:
        model = Board
        fields = [
            'title',
            'contents',
            'board_name'
        ]
        widgets = {
            'contents' : SummernoteWidget()
        }

    def clean(self):
        cleaned_data = super().clean()

        title = cleaned_data.get('title', '')
        contents = cleaned_data.get('contents', '')
        board_name = cleaned_data.get('board_name', 'Consulting Record')

        if title == '':
            self.add_error('title', '글 제목을 입력하세요.')
        elif contents == '':
            self.add_error('contents', '글 내용을 입력하세요.')
        else:
            self.title = title
            self.contents = contents
            self.board_name = board_name
