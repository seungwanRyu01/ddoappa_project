from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages
from django.http import JsonResponse


# 메인 페이지
def home(req):
    if req.session.get('id'):
        check_user = User.objects.get(userid = req.session.get('id'))
        print(req.session.get('id'))
        return render(req, 'home.html', {'session' : req.session.get('id'), 'user_record' : check_user})
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

    login_member = User.objects.filter(userid=req.POST.get('id'), password=req.POST.get('pw'))

    if login_member:
        req.session["id"] = req.POST.get('id')
        print("로그인 성공")
        return redirect('home')
    else:
        messages.error(req, '존재하지 않는 아이디이거나 비밀번호가 일치하지 않습니다.')
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
        return render(req, 'mypage.html', {'mypage':req.session.get('id'), 'infoUser':infoUser})



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
        return render(req, 'deleteUser.html', {'infoUser':infoUser})


# 회원 탈퇴 구현 함수
def deleteUser(req):
    delete_user = User.objects.get(userid=req.POST.get('id'), password=req.POST.get('pw'))

    if delete_user:
        delete_user.delete()
        req.session.pop('id')
        print('회원탈퇴 완료')
        messages.info(req, '회원탈퇴가 정상적으로 완료되었습니다.')
        return redirect('home')