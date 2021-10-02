from django.db import models

# from ckeditor.fields import RichTextField
# from ckeditor_uploader.fields import RichTextUploadingField
# Create your models here.

class User(models.Model):
    userid = models.CharField(max_length=64, unique=True, verbose_name='사용자 아이디')
    password = models.CharField(max_length=64, verbose_name='사용자 비밀번호')
    username = models.CharField(max_length=64, verbose_name='사용자 이름')
    useremail = models.EmailField(max_length=32, unique=True, verbose_name='사용자 이메일')
    phoneNumber = models.CharField(max_length=16, unique = True, verbose_name='사용자 전화번호')
    registered = models.DateTimeField(auto_now_add=True, verbose_name='계정 생성시간')
    GENDERS = (('M', '남성(Man)'), ('W', '여성(Woman)'))
    gender = models.CharField(max_length=1, verbose_name='사용자 성별', choices=GENDERS)
    JOBS = (('W', '직장인(Worker)'), ('A', '선수(Athlete)'), ('S', '학생(Student)'), ('P', '대학원생(Postgrade)'), ('E', '기타(etc)'))
    job = models.CharField(max_length=1, verbose_name='사용자 직업', choices=JOBS)
    FREQUENCY = (('VO', '매우 자주'), ('U', '자주'), ('S', '가끔'), ('H', '거의 안함'), ('N', '안함'))
    exercise_frequency = models.CharField(max_length=2, verbose_name='운동 빈도', choices=FREQUENCY)

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'User'
        verbose_name = '유저'
        verbose_name_plural = '유저'



class Board(models.Model):
    title       = models.CharField(max_length=200, verbose_name="제목")
    contents    = models.TextField(verbose_name="내용")
    writer      = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name="작성자")
    write_dttm  = models.DateTimeField(auto_now_add=True, verbose_name="작성일")
    
    board_name = models.CharField(max_length=32, default='Consulting Record', verbose_name='게시판 종류')
    update_dttm = models.DateTimeField(auto_now=True, verbose_name='최종 수정일')
    hits = models.PositiveIntegerField(default=0, verbose_name='조회수')

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'board'
        verbose_name = '게시판'
        verbose_name_plural = '게시판'



# class ExampleModel(models.Model):
#     content = RichTextUploadingField()

# class ExampleNonUploadModel(models.Model):
#     content = RichTextField()