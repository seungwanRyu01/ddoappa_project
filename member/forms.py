from django import contrib, forms
from django.forms import widgets
from .models import Board
from django import forms
from django_summernote.fields import SummernoteTextField
from django_summernote.widgets import SummernoteWidget

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
        ('Suggestion', '건의 사항'),
        ('Problem', '문제 제기'),
        ('Error', '서비스 에러'),

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
        board_name = cleaned_data.get('board_name', 'Suggestion')

        if title == '':
            self.add_error('title', '글 제목을 입력하세요.')
        elif contents == '':
            self.add_error('contents', '글 내용을 입력하세요.')
        else:
            self.title = title
            self.contents = contents
            self.board_name = board_name
