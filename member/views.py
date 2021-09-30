from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from .models import User, Board
from django.contrib import messages
from django.http import JsonResponse
from .forms import BoardForm
# from django.urls import reverse
# from django.views import generic
# from .models import ExampleModel



# 메인 페이지
def home(req):
    if req.session.get('id'):
        infoUser = User.objects.get(userid = req.session.get('id'))
        print(req.session.get('id'))
        return render(req, 'home.html', {'session' : req.session.get('id'), 'infoUser' : infoUser })
    else:
        return render(req, 'home.html')



# 회원가입
def register(req):
    if req.method == "GET":
        return render(req, 'register.html')

    elif req.method == "POST": # POST로 넘어온 값이 있을 때, 실행
        userid = req.POST.get('id')
        password = req.POST.get('pw')
        username = req.POST.get('name')
        useremail = req.POST.get('email')
        phoneNumber = req.POST.get('pNum')
        gender = req.POST.get('gender')
        job = req.POST.get('job')
        exercise_frequency = req.POST.get('freq')

        # date는 넘길 값
        # data = {}       

        # 변수에 하나라도 빈 값이 있다면 error에 값을 넣어 오류를 출력할 것
        if not (userid and username and password and useremail and phoneNumber and gender and job and exercise_frequency):
            # data['error'] = '모든 값을 입력해주셔야 합니다!'
            messages.error(req, '모든 값을 입력해주셔야 합니다!')
            return render(req, 'register.html')

        elif (req.POST.get('pw') != req.POST.get('chkpw')):
            messages.error(req, '비밀번호 확인이 일치하지 않습니다. 다시 입력해주세요!')
            return render(req, 'register.html')

        else :
            # Model을 객체로 불러와 POST로 넘어온 변수의 값 넣어주기
            user = User(userid = userid, username = username, password = password, gender = gender, useremail = useremail,
                        phoneNumber = phoneNumber, job = job, exercise_frequency = exercise_frequency)
            user.save()
            messages.success(req, '회원가입이 완료되었습니다. 로그인 화면으로 돌아갑니다.')
            return redirect('login')



# 회원가입 아이디 중복체크
def check_id(req):
    userid = req.GET.get('id')
    print(userid)
    try:
        # 중복 검사 실패
        user = User.objects.get(userid = userid)
        print(userid)
    except:
        # 중복 검사 성공
        user = None
    if user is None:
        overlap = "pass"
    else:
        overlap = "fail"
    context = {'duplicate_check': overlap}
    return JsonResponse(context) 



# 로그인
def login(req):
    if req.method == "POST" :
        login_member = User.objects.filter(userid=req.POST.get('id'), password=req.POST.get('pw'))

        if login_member:
            req.session["id"] = req.POST.get('id')
            print("로그인 성공")
            return redirect('home')
        else:
            messages.error(req, '존재하지 않는 아이디이거나 비밀번호가 일치하지 않습니다!')
            return render(req, 'login.html')
    else :
        return render(req, 'login.html')



# 세션 로그아웃
def logout(req):
    try:
        req.session.pop('id') # 세션을 날려버리겠다.
        return redirect('home')
    except KeyError:
        return render(req, 'home.html', {'logout':'정상적인 접근이 아닙니다. 홈화면으로 다시 이동하세요.'})



# 마이 회원 정보 페이지
def myPage(req):
    if req.session.get('id'):
        infoUser = User.objects.get(userid = req.session.get('id'))

        if infoUser.gender == "M":
            infoUser.gender = "남자"
        else:
            infoUser.gender = "여자"

        if infoUser.job == "W":
            infoUser.job = "직장인"
        elif infoUser.job == "A":
            infoUser.job = "선수"
        elif infoUser.job == "S":
            infoUser.job = "학생"
        elif infoUser.job == "P":
            infoUser.job = "대학원생"
        else:
            infoUser.job = "기타"

        if infoUser.exercise_frequency == "U":
            infoUser.exercise_frequency = "자주"
        elif infoUser.exercise_frequency == "S":
            infoUser.exercise_frequency = "가끔"
        elif infoUser.exercise_frequency == "H":
            infoUser.exercise_frequency = "거의 안함"
        else:
            infoUser.exercise_frequency = "안함"
        
        return render(req, 'mypage.html', {'session': req.session.get('id'), 'infoUser' : infoUser})



# 회원정보 수정 페이지
def updateUserPage(req):
    if req.session.get('id'):
        infoUser = User.objects.get(userid = req.session.get('id'))
        return render(req, 'updateUser.html', {'infoUser':infoUser} )



# 회원정보 수정 함수
def updateUser(req):
    change_user = User.objects.get(userid = req.POST.get('id'), password = req.POST.get('pw'))
    print(change_user)

    if change_user:
        change_user.password = req.POST.get('new_pw')
        change_user.username = req.POST.get('new_name')
        change_user.useremail = req.POST.get('new_email')
        change_user.phoneNumber = req.POST.get('new_pNum')
        change_user.job = req.POST.get('new_job')
        change_user.exercise_frequency = req.POST.get('new_freq')

        change_user.save()
    
        messages.info(req, '회원정보 수정이 완료되었습니다.')
        return redirect('mypage')



# 회원 탈퇴 페이지
def deleteUserPage(req):
    if req.session.get('id'):
        infoUser = User.objects.get(userid = req.session.get('id'))
        return render(req, 'deleteUser.html', {'infoUser': infoUser})



# 회원 탈퇴 구현 함수
def deleteUser(req):
    delete_user = User.objects.get(userid=req.POST.get('id'), password=req.POST.get('pw'))

    if delete_user:
        delete_user.delete()
        req.session.pop('id')
        print('회원탈퇴 완료')
        messages.info(req, '회원탈퇴가 정상적으로 완료되었습니다.')
        return redirect('home')



def board_list(req):
    if req.session.get('id'):
        infoUser = User.objects.get(userid = req.session.get('id'))
        boards= Board.objects.all().order_by('-id')
        return render(req, 'board_list.html', {'session' : req.session.get('id'), 'infoUser' : infoUser, 'boards' : boards })
    else:
        boards= Board.objects.all().order_by('-id')
        return render(req, 'board_list.html', {'session' : req.session.get('id'), 'boards' : boards })



def board_write(req):
    if req.method == "POST":
        form = BoardForm(req.POST)

        if form.is_valid():
            # form의 모든 validators 호출 유효성 검증 수행
            user_id = req.session.get('id')
            member = User.objects.get(pk=user_id)
            print(user_id)
            
            board = Board()
            board.title    = form.cleaned_data['title']
            board.contents = form.cleaned_data['contents']

            # 검증에 성공한 값들은 사전타입으로 제공 (form.cleaned_data)
            # 검증에 실패시 form.error 에 오류 정보를 저장
            
            board.writer = member
            board.save()

            return redirect('../boardlist/')

    else:
        form = BoardForm()

    return render(req, 'board_write.html', {'form' : form})



# class CKEditorFormView(generic.FormView):
#     form_class = forms.CkEditorForm
#     template_name = "form.html"

#     def post(self, req):
#         content = ExampleModel(content = req.POST.get("ckeditor_standard_example"))
#         content.save()
#         return HttpResponse("ok")

#     def get_success_url(self):
#         return reverse("ckeditor-form")

# ckeditor_form_view = CKEditorFormView.as_view()