from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from django.core.paginator import Paginator

from .models import SelfIntroduction
from .models import FreeBoard
from .models import QuestionBoard
from .Result_Code import Final_Keyword_Similarity
from .Result_Code import Cos
from .Result_Code import Grammar
# Create your views here.

# 메인 페이지
def index(request):
    # 사용자정보 로드
    username = None
    if request.session.get('user'):  # 로그인 중이면
        username = User.objects.get(pk=request.session.get('user'))  # 사용자 이름 저장

    return render(request, 'index.html', {'username': username})

# 회원가입
def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username', None)
        useremail = request.POST.get('useremail', None)
        password = request.POST.get('password', None)
        repassword = request.POST.get('repassword', None)
        try:
            if not (username and useremail and password and repassword):
                errorMsg = '빈칸이 존재합니다. 모두 입력하세요.'
            elif password != repassword:
                errorMsg = '비밀번호가 다릅니다.'
            else:
                User.objects.create_user(
                    username=username,
                    email=useremail,
                    password=password
                )
                return redirect('/login')
        except:
            errorMsg = '이미 존재하는 아이디 입니다.'
        return render(request, 'signup.html', {'error': errorMsg})

    return render(request, 'signup.html')

# 로그인
def login(request):
    # POST 요청시
    if request.method == 'POST':                                        # 로그인 버튼 클릭
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)

        try:
            if not (username and password):                             # 아이디/비밀번호 중 빈칸이 존재할 때
                errorMsg = '아이디/비밀번호를 입력하세요.'
            else:                                                       # 아이디/비밀번호 모두 입력됐을 때
                user = User.objects.get(username = username)            # 등록된 아이디의 정보 가져오기
                if check_password(password, user.password):             # 등록된 아이디의 비밀번호가 맞으면
                    request.session['user'] = user.id                   # 세션에 아이디 추가
                    request.session['email'] = user.email               # 세션에 이메일 추가
                    return redirect('/')                                # 메인 페이지 이동
                else:                                                   # 등록된 아이디의 비밀번호가 틀리면
                    errorMsg = '비밀번호가 틀렸습니다.'
        except:                                                         # 등록된 아이디의 정보가 없을 때
            errorMsg = '가입하지 않은 아이디 입니다.'

        return render(request, 'login.html', {'error': errorMsg})   # 에러 메세지와 로그인 페이지(login.html) 리턴
    # GET 요청시
    return render(request, 'login.html')                            # 로그인 페이지(login.html) 리턴

# 로그아웃
def logout(request):
    del(request.session['user'])    # 세션에서 사용자정보 삭제
    return redirect('/')            # 메인 페이지(index.html) 리턴

# 비밀번호 재설정 (비밀번호 재설정 페이지 중복)
def repassword(request):
    session_user_info = User.objects.get(pk=request.session.get('user'))

    # POST 요청시
    if request.method == 'POST':                                        # 비밀번호 변경 버튼 클릭
        my_pass = request.POST.get('password', None)                    # 현재 비밀번호
        change_pass = request.POST.get('change_password', None)         # 변경할 비밀번호
        re_change_pass = request.POST.get('re_change_password', None)   # 변경할 비밀번호 확인

        if not (my_pass and change_pass and re_change_pass):            # 모든 정보가 입력되지 않았을 때
            errorMsg = '비밀번호를 입력하세요'
        else:                                                           # 모든 정보가 입력됐을 때
            user = User.objects.get(pk=request.session.get('user'))     # 세션에서 유저 정보 가져오기
            if check_password(my_pass, user.password):                  # 현재 비밀번호 체크
                if change_pass == re_change_pass:                       # 비밀번호 확인 체크
                    user.set_password(change_pass)                      # 비밀번호 변경
                    user.save()                                         # 비밀번호 저장
                    return redirect('/')                          # 내 정보 페이지(myinfo.html) 리턴 추후추가
                else:
                    errorMsg = '변경할 비밀번호가 서로 다릅니다.'
            else:
                errorMsg = '비밀번호가 틀립니다.'

        return render(request, 'repassword.html', {'error': errorMsg, 'username': session_user_info})
    # GET 요청시
    return render(request, 'repassword.html', {'username': session_user_info})

# 비밀번호 재설정 (비밀번호 재설정 페이지 중복)
def password(request):
    return render(request, 'password.html')

# 비밀번호 재설정 (비밀번호 재설정 페이지 중복)
def resetpassword(request):
    return render(request, 'resetpassword.html')

# 내 정보
def myinfo(request):
    username = User.objects.get(pk=request.session.get('user'))         # 사용자 이름
    useremail = request.session.get('email')                            # 사용자 Email
    return render(request, 'myinfo.html', {'username': username, 'email': useremail, 'msg': username})

def myinfo_edit(request):
    if request.method == "POST":
        user = request.user
        user.id = request.POST["username"]
        user.password = request.POST["password"]
        user.email = request.POST["useremail"]
        user.save()
        return redirect('/')
    return render(request,'myinfo_edit')

########################################################################################################################
import os
# 초기데이터 삽입(임시 1회만 사용할 코드)
def initial_data_insert(request):

    BASE_DIR = f'../../../Final/07_Saramin_dataset/dataset'

    title = f'INITIAL PASSED DATA'
    username = User.objects.get(pk=request.session.get('user'))
    pass_fail_result = ('PASS')

    current_num = 0
    for file in os.listdir(BASE_DIR):
        current_num += 1
        print(f'{BASE_DIR}/{file} Inserting... ({current_num}/{len(os.listdir(BASE_DIR))})')
        fopen = open(f'{BASE_DIR}/{file}', 'r', encoding='utf-8').readlines()
        company_name = fopen[0]
        department_name = fopen[1]
        contents = '\n'.join(fopen[2:])

        new_introduction = SelfIntroduction.objects.create(
            title=title,
            name=username,
            pass_fail_result=pass_fail_result,
            company_name=company_name,
            department_name=department_name,
            contents=contents
        )
        new_introduction.save()

    return render(request, 'index.html')

########################################################################################################################
# Free Board 게시판
def freeboard(request):
    # 사용자정보 로드
    username = None
    if request.session.get('user'):                                     # 로그인 중이면
        username = User.objects.get(pk=request.session.get('user'))     # 사용자 이름 저장

    # 페이지정보 로드
    all_freeboard_posts = FreeBoard.objects.all().order_by('-id')       # 모든 자유게시판 데이터를 id순으로 가져오기
    paginator = Paginator(all_freeboard_posts, 10)                      # 한 페이지에 10개씩 정렬
    page = int(request.GET.get('p', 1))                                 # p번 페이지 값, p값 없으면 1 반환
    posts = paginator.get_page(page)                                    # p번 페이지 가져오기

    # 자유 게시판 페이지(freeboard.html) 리턴
    return render(request, 'freeboard.html',
                  {'posts': posts, 'username': username})

# Free Board 게시글 쓰기
def freeboard_writing(request):
    # 사용자정보 로드
    username = None
    if request.session.get('user'):                                     # 로그인 중이면
        username = User.objects.get(pk=request.session.get('user'))     # 사용자 이름 저장
    # POST 요청시
    if request.method =='POST':
        # 새 게시글 객체 생성
        new_post = FreeBoard.objects.create(
            title=request.POST['title'],
            contents=request.POST['contents'],
            name=User.objects.get(pk=request.session.get('user')),
        )
        return redirect(f'/freeboard_post/{new_post.id}')               # 해당 게시글 페이지로 이동

    # GET 요청시 글쓰기 페이지(writing.html) 리턴
    return render(request, 'freeboard_writing.html', {'username' : username})

# Free Board 게시글 보기
def freeboard_post(request, pk):
    # 사용자정보 로드
    username = None
    if request.session.get('user'):                                     # 로그인 중이면
        username = User.objects.get(pk=request.session.get('user'))     # 사용자 이름 저장

    # 게시글 정보 로드
    post = get_object_or_404(FreeBoard, pk=pk)

    # 해당 게시글 페이지(freeboard_post.html) 반환
    return render(request, 'freeboard_post.html',
                  {'post' : post, 'username' : username})

# Free Board 게시글 수정
def freeboard_edit(request, pk):
    # 사용자정보 로드
    username = None
    if request.session.get('user'):                                     # 로그인 중이면
        username = User.objects.get(pk=request.session.get('user'))     # 사용자 이름 저장

    # 게시글 정보 로드
    post = FreeBoard.objects.get(pk=pk)

    # POST 요청시
    if request.method=="POST":
        post.title = request.POST['title']                              # 제목 수정 반영
        post.contents = request.POST['contents']                        # 내용 수정 반영
        post.save()                                                     # 수정된 내용 저장
        return redirect(f'/freeboard_post/{pk}')                        # 해당 게시글 페이지로 이동

    # GET 요청시 게시글 수정 페이지(postedit.html) 리턴
    return render(request, 'freeboard_edit.html', {'post':post, 'username' : username})

# Free Board 게시글 삭제
def freeboard_delete(request, pk):
    post = FreeBoard.objects.get(id=pk)                                 # 해당 게시글 테이블 저장
    post.delete()                                                       # 해당 게시글 삭제
    return redirect(f'/freeboard')                                      # 자유 게시판 페이지로 이동

########################################################################################################################
# Q & A 게시판
def questionboard(request):
    # 사용자정보 로드
    username = None
    if request.session.get('user'):                                         # 로그인 중이면
        username = User.objects.get(pk=request.session.get('user'))         # 사용자 이름 저장

    # 페이지정보 로드
    all_questionboard_posts = QuestionBoard.objects.all().order_by('-id')   # 모든 자유게시판 데이터를 id순으로 가져오기
    paginator = Paginator(all_questionboard_posts, 10)                      # 한 페이지에 10개씩 정렬
    page = int(request.GET.get('p', 1))                                     # p번 페이지 값, p값 없으면 1 반환
    posts = paginator.get_page(page)                                        # p번 페이지 가져오기

    # 자유 게시판 페이지(freeboard.html) 리턴
    return render(request, 'questionboard.html',
                  {'posts': posts, 'username': username})

# Q & A 게시글 쓰기
def questionboard_writing(request):
    # 사용자정보 로드
    username = None
    if request.session.get('user'):                                         # 로그인 중이면
        username = User.objects.get(pk=request.session.get('user'))         # 사용자 이름 저장
    # POST 요청시
    if request.method =='POST':
        # 새 게시글 객체 생성
        new_post = QuestionBoard.objects.create(
            title=request.POST['title'],
            contents=request.POST['contents'],
            name=User.objects.get(pk=request.session.get('user')),
        )
        return redirect(f'/questionboard_post/{new_post.id}')               # 해당 게시글 페이지로 이동

    # GET 요청시 글쓰기 페이지(writing.html) 리턴
    return render(request, 'questionboard_writing.html', {'username' : username})

# Q & A 게시글 보기
def questionboard_post(request, pk):
    # 사용자정보 로드
    username = None
    if request.session.get('user'):                                         # 로그인 중이면
        username = User.objects.get(pk=request.session.get('user'))         # 사용자 이름 저장

    # 게시글 정보 로드
    post = get_object_or_404(QuestionBoard, pk=pk)


    # 해당 게시글 페이지(freeboard_post.html) 리턴
    return render(request, 'questionboard_post.html',
                  {'post' : post, 'username' : username})

# Q & A 게시글 수정
def questionboard_edit(request, pk):
    # 사용자정보 로드
    username = None
    if request.session.get('user'):                                         # 로그인 중이면
        username = User.objects.get(pk=request.session.get('user'))         # 사용자 이름 저장

    # 게시글 정보 로드
    post = QuestionBoard.objects.get(pk=pk)

    # POST 요청시
    if request.method=="POST":
        post.title = request.POST['title']                                  # 제목 수정 반영
        post.contents = request.POST['contents']                            # 내용 수정 반영
        post.save()                                                         # 수정된 내용 저장
        return redirect(f'/questionboard_post/{pk}')                        # 해당 게시글 페이지로 이동
    # GET 요청시 게시글 수정 페이지(postedit.html) 리턴
    return render(request, 'questionboard_edit.html', {'post':post, 'username' : username})

# Q & A 게시글 삭제
def questionboard_delete(request, pk):
    post = QuestionBoard.objects.get(id=pk)                                 # 해당 게시글 테이블 저장
    post.delete()                                                           # 해당 게시글 삭제
    return redirect(f'/questionboard')                                      # 자유 게시판 페이지로 이동

########################################################################################################################
# 자기소개서 목록
def selfintroboard(request):
    # 사용자 정보 로드
    uesername = None
    if request.session.get('user'):
        username = User.objects.get(pk=request.session.get('user'))

    # 페이지정보 로드
    all_selfintro_posts = SelfIntroduction.objects.all().order_by('-id')    # 모든 자기소개서 데이터를 id 순으로 가져오기
    paginator = Paginator(all_selfintro_posts, 10)                          # 한 페이지에 10개씩 정렬
    page = int(request.GET.get('p', 1))                                     # p번 페이지 값, p값 없으면 1 반환
    posts = paginator.get_page(page)                                        # p번 페이지 가져오기

    # 자기소개서 목록 페이지(selfintroboard.html) 리턴
    return render(request, 'selfintroboard.html',
                  {'posts' : posts, 'username' : username})

# 자소서 쓰기
def selfintroboard_writing(request):
    # 사용자정보 로드
    username = None
    if request.session.get('user'):                                     # 로그인 중이면
        username = User.objects.get(pk=request.session.get('user'))     # 사용자 이름 저장
    # POST 요청시
    if request.method =='POST':
        # 새 게시글 객체 생성
        new_selfintro = SelfIntroduction.objects.create(
            title=request.POST['title'],
            company_name=request.POST['company_name'],
            department_name=request.POST['department_name'],
            contents=request.POST['contents'],
            name=User.objects.get(pk=request.session.get('user')),
        )
        return redirect(f'/selfintroboard_save/{new_selfintro.id}')

    # GET 요청시 글쓰기 페이지(writing.html) 리턴
    return render(request, 'selfintroboard_writing.html', {'username' : username})

# 자소서 보기
def selfintroboard_post(request, pk):
    # 사용자정보 로드
    username = None
    if request.session.get('user'):                                     # 로그인 중이면
        username = User.objects.get(pk=request.session.get('user'))     # 사용자 이름 저장

    # 자소서 정보 로드
    post = get_object_or_404(SelfIntroduction, pk=pk)

    return render(request, 'selfintroboard_post.html',
                  {'post' : post, 'username' : username})

# 자소수 수정
def selfintroboard_edit(request, pk):
    # 사용자정보 로드
    username = None
    if request.session.get('user'):                                     # 로그인 중이면
        username = User.objects.get(pk=request.session.get('user'))     # 사용자 이름 저장

    post = SelfIntroduction.objects.get(pk=pk)

    # POST 요청시
    if request.method=='POST':
        post.title = request.POST['title']                      # 제목 수정 반영
        post.company_name = request.POST['company_name']        # 기업 수정 반영
        post.department_name = request.POST['department_name']  # 직무 수정 반영
        post.contents = request.POST['contents']                # 내용 수정 반영
        post.save()                                             # 수정된 내용 저장
        return redirect(f'/selfintroboard_save/{post.id}')           # 해당 자소서 페이지로 이동

    # GET 요청시 자소서 수정 페이지 (selfintroboard_edit.html) 리턴
    return render(request, 'selfintroboard_edit.html',
                  {'post' : post, 'username' : username})

# 자소서 저장
def selfintroboard_save(request, pk):
    # 사용자정보 로드
    username = None
    if request.session.get('user'):                                     # 로그인 중이면
        username = User.objects.get(pk=request.session.get('user'))     # 사용자 이름 저장

    post = get_object_or_404(SelfIntroduction, pk=pk)

    return render(request, 'selfintroboard_save.html',
                  {'post' : post, 'username' : username})

# 자소서 삭제
def selfintroboard_delete(request, pk):
    post = SelfIntroduction.objects.get(id=pk)                                 # 해당 게시글 테이블 저장
    post.delete()                                                           # 해당 게시글 삭제
    return redirect(f'/selfintroboard')                                      # 자유 게시판 페이지로 이동

# 자소서 분석 결과
def selfintroboard_result(request, pk):
    # 사용자정보 로드
    username = None
    if request.session.get('user'):  # 로그인 중이면
        username = User.objects.get(pk=request.session.get('user'))  # 사용자 이름 저장

    post = get_object_or_404(SelfIntroduction, pk=pk)
    in_keyword, not_in_keyword, keyword_percent = Final_Keyword_Similarity.Keyword_Similarity(post.company_name, post.contents)

    pass_intros = []
    for pi in SelfIntroduction.objects.all():
        if pi.pass_fail_result == 'PASS':
            pass_intros.append(pi.contents)

    plagiarism_percent = Cos.plagiarism_check(post.contents, pass_intros)
    grammar_result = Grammar.grammar_run(post.contents)

    if plagiarism_percent > 30:
        plagiarism_comment = "표절률이 높습니다. 표절률이 높으면 서류 합격확률이 낮아질 수 있습니다."
    else:
        plagiarism_comment = ""
    comment = "("+', '.join(not_in_keyword) + ")의 키워드가 존재하지 않습니다. \"" + post.company_name + "\"의 기업에서 요구하는 인재상을 본문에 강조하면" \
                                                                                      " 적합률이 올라갈 수 있습니다." + "\n" + plagiarism_comment

    return render(request, 'selfintroboard_result.html',
                  {'post': post, 'username': username, 'keyword_percent': keyword_percent,
                   'plagiarism_percent': plagiarism_percent,
                   'grammar_result': grammar_result, 'comment' : comment})
########################################################################################################################