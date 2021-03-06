from django.core import paginator
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect, resolve_url
from .models import User, Board
from django.contrib import messages
from django.http import JsonResponse
from .forms import BoardWriteForm
from .decorators import login_required
from datetime import date, datetime, timedelta
from django.core.paginator import Paginator
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



# 게시판 목록
def board_list(req):
    login_session = req.session.get('id', '')
    context = {'session' : login_session }

    boards_all = Board.objects.order_by('-id')
    page = int(req.GET.get('p',1)) #이 없으면 1로 지정
    paginator = Paginator(boards_all, 5) # 한 페이지당 5개씩 보여줌
    boards = paginator.get_page(page)

    context['boards'] = boards

    return render(req, 'board_list.html', context)



# 게시판 글쓰기
@login_required
def board_write(req):
    login_session = req.session.get('id', '')
    infoUser = User.objects.get(userid = req.session.get('id'))
    context = {'session' : login_session }

    if req.method == 'GET':
        write_form  = BoardWriteForm()
        context['forms'] = write_form
        return render(req, 'board_write.html', context)

    elif req.method == 'POST':
        write_form = BoardWriteForm(req.POST)

        if write_form.is_valid():
            writer = User.objects.get(userid = login_session)
            board = Board(
                title = write_form.title,
                contents = write_form.contents,
                writer = writer,
                board_name = write_form.board_name
            )
            board.save()
            return redirect('../boardlist')
        else:
            context['forms'] = write_form
            if write_form.errors:
                for value in write_form.errors.values():
                    context['error'] = value
            return render(req, 'board_write.html', {'infoUser' : infoUser }, context)



# 게시판 상세 페이지
def board_detail(req, pk):
    login_session = req.session.get('id', '')
    context = {'session' : login_session }

    board = get_object_or_404(Board, id=pk)
    context['board'] = board

    # 글쓴이인지 확인
    if board.writer.userid == login_session:
        context['writer'] = True
    else:
        context['writer'] = False

    response = render(req, 'board_detail.html', context)

    # 조회수 기능 체크 (쿠키 이용)
    expire_date, now = datetime.now(), datetime.now()
    expire_date += timedelta(days=1)
    expire_date = expire_date.replace(hour=0, minute=0, second=0, microsecond=0)
    expire_date -= now
    max_age = expire_date.total_seconds()

    cookie_value = req.COOKIES.get('hitboard', '_')

    if f'_{pk}_' not in cookie_value:
        cookie_value += f'_{pk}_'
        response.set_cookie('hitboard', value=cookie_value, max_age=max_age, httponly=True)
        board.hits += 1
        board.save()

    return response



# 게시판 글 삭제
def board_delete(req, pk):
    login_session = req.session.get('id', '')

    board = get_object_or_404(Board, id=pk)
    if board.writer.userid == login_session:
        board.delete()
        return redirect('boardlist')
    else:
        return redirect(f'boardlist/boarddetail/{pk}/')



# 게시판 글 수정
@login_required
def board_edit(req, pk):
    login_session = req.session.get('id', '')
    context = {'session' : login_session }

    board = get_object_or_404(Board, id=pk)
    context['board'] = board

    if board.writer.userid != login_session:
        return redirect(f'boardlist/boarddetail/{pk}/')

    if req.method == 'GET':
        write_form = BoardWriteForm(instance=board)
        context['forms'] = write_form
        return render(req, 'board_edit.html', context)

    elif req.method == 'POST':
        write_form = BoardWriteForm(req.POST)

        if write_form.is_valid():

            board.title = write_form.title
            board.contents = write_form.contents
            board.board_name = write_form.board_name

            board.save()
            return redirect('boardlist')

        else:
            context['forms'] = write_form
            if write_form.errors:
                for value in write_form.errors.values():
                    context['error'] = value
            return render(req, 'board_edit.html', context)



def map_search(req):
    return render(req, 'map_search.html')


def card_list(req):
    return render(req, 'card_list.html')



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