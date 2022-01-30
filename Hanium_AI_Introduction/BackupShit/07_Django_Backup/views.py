from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from django.core.paginator import Paginator
from . models import Post, Self_introduction, Plagiarism_result, Grammar_result, Pass_result
from . import Plagiarism, Grammar

# Create your views here.
########################################################################################################################
# 사용자이름 전달(로그인 중일 때)
def username_passing(request):
    if request.session.get('user'):                                     # 로그인 중이면
        username = User.objects.get(pk=request.session.get('user'))     # 사용자 이름 저장
        return username                                                 # 사용자 이름 리턴
########################################################################################################################
# 로그인 (추가수정: 마지막라인 return은 원래 여기 있어서는 안됨, html 단계에서 넘어가야함)
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

        return render(request, 'app/login.html', {'error': errorMsg})   # 에러 메세지와 로그인 페이지(login.html) 리턴
    # GET 요청시
    return render(request, 'app/login.html')                            # 로그인 페이지(login.html) 리턴

# 로그아웃
def logout(request):
    del(request.session['user'])    # 세션에서 사용자정보 삭제
    return redirect('/')            # 메인 페이지(index.html) 리턴

# 회원가입 (추가수정: 마지막라인 return은 원래 여기 있어서는 안됨, html 단계에서 넘어가야함)
def register(request):
    # POST 요청시
    if request.method == 'POST':                                # 계정 만들기 버튼 클릭
        username = request.POST.get('username', None)           # 아이디
        useremail = request.POST.get('useremail', None)         # 이메일
        password = request.POST.get('password', None)           # 비밀번호
        repassword = request.POST.get('re-password', None)      # 비밀번호 재입력
        try:
            if not (username and useremail and password and repassword):    # 모든 정보가 입력되지 않았을 때
                errorMsg = '빈칸이 존재합니다. 모두 입력하세요.'
            elif password != repassword:                    # 비밀번호가 다를 때
                errorMsg = '비밀번호가 다릅니다.'
            else:                                           # 모든 정보가 입력됐을 때
                User.objects.create_user(                   # 유저 데이터 생성
                    username = username,
                    email = useremail,
                    password = password)
                return redirect('/login')                   # 로그인 페이지로 이동

        except:                                             # 유저 데이터가 이미 존재할 때
            errorMsg = '이미 존재하는 아이디 입니다.'
        return render(request, 'app/register.html', {'error': errorMsg}) # 에러메세지와 회원가입 페이지(register.html) 리턴
    # GET 요청시
    return render(request, 'app/register.html')             # 회원가입 페이지(register.html) 리턴

# 비밀번호 찾기 (미구현)
def password(request):
    return render(request, 'app/password.html')

# 보안상의 이유로 사용한다면 함수로 작성할 것을 권고
# 여기까지 처리하다 중단함
def pass_modify(request):
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
                    return redirect('/myinfo')                          # 내 정보 페이지(myinfo.html) 리턴
                else:
                    errorMsg = '변경할 비밀번호가 서로 다릅니다.'
            else:
                errorMsg = '비밀번호가 틀립니다.'

        return render(request, 'app/modify.html', {'error': errorMsg, 'username': session_user_info})
    # GET 요청시
    return render(request, 'app/modify.html', {'username': session_user_info})

# 내 정보
def myinfo(request):
    username = User.objects.get(pk=request.session.get('user'))         # 사용자 이름
    useremail = request.session.get('email')                            # 사용자 Email
    return render(request, 'app/myinfo.html', {'username': username, 'email': useremail, 'msg': username})
########################################################################################################################
# 메인 페이지
def index(request):
    username = username_passing(request)                                    # 로그인 중이면 사용자이름 저장
    return render(request,'app/index.html', {'username' : username})        # 메인 페이지(index.html) 리턴

# 개발자 소개
def developer(request):
    username = username_passing(request)
    return render(request, 'app/developer.html', {'username' : username})   # 개발자 소개 페이지(developer.html) 리턴
########################################################################################################################
# 맞춤법 검사
def grammar(request):
    username = username_passing(request)                                        # 유저이름 불러오기
    all_self_intro = Self_introduction.objects.all().order_by('-id')        # 모든 자기소개서 데이터를 id순으로 가져오기
    paginator = Paginator(all_self_intro, 10)                               # 한 페이지에 10개씩 정렬
    page = int(request.GET.get('p', 1))                                     # 1번 페이지 값
    self_intros = paginator.get_page(page)                                  # 1번 페이지 가져오기

    # 맞춤법 검사 페이지(grammar.html) 리턴
    return render(request, 'app/grammar.html', {'username' : username, 'self_intros' : self_intros})

# 맞춤법 검사 상세확인 (구현작업중)
def grammar_detail(request, pk):
    username = username_passing(request)                                        # 유저이름 불러오기
    self_intro = get_object_or_404(Self_introduction, pk=pk)                    # 해당유저 자소서 불러오기, pk는 해당 객체 고유 id값
    grammar_results = get_object_or_404(Grammar_result, id_value=pk)      # 해당유저 자소서 표절검사 결과 id값을 통해 불러오기

    return render(request, 'app/grammar_detail.html', {'self_intro' : self_intro, 'username' : username, 'grammar_results' : grammar_results})

# 표절검사 게시판
def plagiarism(request):
    username = username_passing(request)                                    # 유저이름 불러오기
    all_self_intro = Self_introduction.objects.all().order_by('-id')        # 모든 자기소개서 데이터를 id순으로 가져오기
    paginator = Paginator(all_self_intro, 10)                               # 한 페이지에 10개씩 정렬
    page = int(request.GET.get('p', 1))                                     # 1번 페이지 값
    self_intros = paginator.get_page(page)                                  # 1번 페이지 가져오기

    # 표절 검사(plagiarism.html) 리턴
    return render(request, 'app/plagiarism.html', {'self_intros' : self_intros, 'username' : username})

# 표절검사 상세확인
def plagiarism_detail(request, pk):
    username = username_passing(request)                                        # 유저이름 불러오기
    self_intro = get_object_or_404(Self_introduction, pk=pk)                    # 해당유저 자소서 불러오기, pk는 해당 객체 고유 id값
    plagiarism_results = get_object_or_404(Plagiarism_result, id_value=pk)      # 해당유저 자소서 표절검사 결과 id값을 통해 불러오기

    return render(request, 'app/plagiarism_detail.html', {'self_intro' : self_intro, 'username' : username, 'plagiarism_results' : plagiarism_results})

# 합격 & 불합격 게시판
def pass_or_fail(request):
    username = username_passing(request)                                    # 유저이름 불러오기
    all_self_intro = Self_introduction.objects.all().order_by('-id')        # 모든 자기소개서 데이터를 id순으로 가져오기
    paginator = Paginator(all_self_intro, 10)                               # 한 페이지에 10개씩 정렬
    page = int(request.GET.get('p', 1))                                     # 1번 페이지 값
    self_intros = paginator.get_page(page)                                  # 1번 페이지 가져오기

    # 합격 & 불합격 페이지(pass.html) 리턴
    return render(request, 'app/pass.html', {'self_intros' : self_intros, 'username' : username})

# 합격 & 불합격 상세확인
def pass_or_fail_detail(request, pk):
    username = username_passing(request)                                        # 유저이름 불러오기
    self_intro = get_object_or_404(Self_introduction, pk=pk)                    # 해당유저 자소서 불러오기, pk는 해당 객체 고유 id값
    pass_results = get_object_or_404(Pass_result, id_value=pk)                  # 해당유저 자소서 표절검사 결과 id값을 통해 불러오기

    return render(request, 'app/pass_detail.html', {'self_intro' : self_intro, 'username' : username, 'pass_results' : pass_results})

# 추천 답변
def recommend(request):
    username = username_passing(request)                                        # 유저이름 불러오기
    return render(request, 'app/recommend.html', {'username' : username})       # 추천 답변(recommend.html) 리턴
########################################################################################################################
# 자기소개서 리스트
def myintro_list(request):
    username = username_passing(request)

    all_self_intro = Self_introduction.objects.all().order_by('-id')    # 모든 자기소개서 데이터를 id순으로 가져오기
    paginator = Paginator(all_self_intro, 10)                           # 한 페이지에 10개씩 정렬
    page = int(request.GET.get('p', 1))                                 # 1번 페이지 값
    self_intros = paginator.get_page(page)                              # 1번 페이지 가져오기

    # 내 자기소개서 페이지(myintro.html)로 이동
    return render(request, 'app/myintro.html', {'self_intros': self_intros, 'username' : username})

# 자기소개서 등록
def function(request):
    username = username_passing(request)
    # POST 요청시
    if request.method =='POST':

        # 새로운 자소서 객체 생성
        new_si = Self_introduction.objects.create(
            title=request.POST.get('title', ''),                        # 제목 저장
            name=User.objects.get(pk=request.session.get('user')),      # 사용자 이름 저장

            # 질문 저장
            question_1=request.POST.get('question_1', ''),
            question_2=request.POST.get('question_2', ''),
            question_3=request.POST.get('question_3', ''),
            question_4=request.POST.get('question_4', ''),
            question_5=request.POST.get('question_5', ''),

            # 답변 저장
            answer_1=request.POST.get('answer_1', ''),
            answer_2=request.POST.get('answer_2', ''),
            answer_3=request.POST.get('answer_3', ''),
            answer_4=request.POST.get('answer_4', ''),
            answer_5=request.POST.get('answer_5', ''),
        )

        # 새로운 자소서 표절 검사 결과 객체 생성
        new_plagiarism_result = Plagiarism_result.objects.create(
            title=request.POST.get('title', ''),                        # 제목 저장
            name=User.objects.get(pk=request.session.get('user')),      # 사용자 이름 저장
            id_value=new_si.id,                                         # 표절검사 결과를 불러오기 위해 검사할 자소서 id값 저장

            plagiarism_result1=Plagiarism.run(request.POST.get('answer_1', '')),
            plagiarism_result2=Plagiarism.run(request.POST.get('answer_2', '')),
            plagiarism_result3=Plagiarism.run(request.POST.get('answer_3', '')),
            plagiarism_result4=Plagiarism.run(request.POST.get('answer_4', '')),
            plagiarism_result5=Plagiarism.run(request.POST.get('answer_5', '')),
        )

        # 새로운 자소서 맞춤법 검사 결과 객체 생성
        new_grammar_result = Grammar_result.objects.create(
            title=request.POST.get('title', ''),                        # 제목 저장
            name=User.objects.get(pk=request.session.get('user')),      # 사용자 이름 저장
            id_value=new_si.id,                                         # 맞춤법 검사 결과를 불러오기 위해 검사할 자소서 id값 저장

            grammar_result1=Grammar.run(request.POST.get('answer_1', '')),
            grammar_result2=Grammar.run(request.POST.get('answer_2', '')),
            grammar_result3=Grammar.run(request.POST.get('answer_3', '')),
            grammar_result4=Grammar.run(request.POST.get('answer_4', '')),
            grammar_result5=Grammar.run(request.POST.get('answer_5', '')),
        )

        # 새로운 자소서 합격 & 불합격 결과 객체 생성
        new_pass_result = Pass_result.objects.create(
            title=request.POST.get('title', ''),                        # 제목 저장
            name=User.objects.get(pk=request.session.get('user')),      # 사용자 이름 저장
            id_value=new_si.id,                                         # 합격 & 불합격 결과를 불러오기 위해 검사할 자소서 id값 저장

            pass_result1='미구현',
            pass_result2='미구현',
            pass_result3='미구현',
            pass_result4='미구현',
            pass_result5='미구현',
        )

        return redirect('/myintro')                                         # 내 자기소개서 페이지 이동
    # GET 요청시
    return render(request, 'app/function.html', {'username' : username})    # 자기소개서 등록 페이지(function.html) 리턴

# 자기소개서 보기
def myintro_detail(request, pk):
    username = username_passing(request)                                    # 유저이름 불러오기
    self_intro = get_object_or_404(Self_introduction, pk=pk)                # 해당유저 자소서 불러오기, pk는 해당 객체 고유 id값
    return render(request, 'app/myintrodetail.html', {'self_intro' : self_intro, 'username' : username})

# 자기소개서 수정
def myintro_edit(request, pk):
    username = username_passing(request)                                    # 유저이름 불러오기
    self_intro = get_object_or_404(Self_introduction, pk=pk)                # 해당유저 자소서 불러오기, pk는 해당 객체 고유 id값
    plagiarism_results = get_object_or_404(Plagiarism_result, id_value=pk)  # 해당유저 자소서 표절검사 결과 id값을 통해 불러오기
    grammar_results = get_object_or_404(Grammar_result, id_value=pk)        # 해당유저 자소서 맞춤법 검사 결과 id값을 통해 불러오기
    pass_results = get_object_or_404(Grammar_result, id_value=pk)           # 해당유저 자소서 합격 & 불합격 결과 id값을 통해 불러오기

    # POST 요청시
    if request.method == "POST":                                            # POST 요청이면 자기소개서 수정

        # 수정된 내용 반영하기
        self_intro.title=request.POST['title']                              
        self_intro.question_1 = request.POST['question_1']
        self_intro.question_2 = request.POST['question_2']
        self_intro.question_3 = request.POST['question_3']
        self_intro.question_4 = request.POST['question_4']
        self_intro.question_5 = request.POST['question_5']

        self_intro.answer_1 = request.POST['answer_1']
        self_intro.answer_2 = request.POST['answer_2']
        self_intro.answer_3 = request.POST['answer_3']
        self_intro.answer_4 = request.POST['answer_4']
        self_intro.answer_5 = request.POST['answer_5']
        self_intro.save()

        # 수정된 내용에 따라 수정된 표절검사 결과 반영하기
        plagiarism_results.plagiarism_result1 = Plagiarism.run(request.POST.get('answer_1', ''))
        plagiarism_results.plagiarism_result2 = Plagiarism.run(request.POST.get('answer_2', ''))
        plagiarism_results.plagiarism_result3 = Plagiarism.run(request.POST.get('answer_3', ''))
        plagiarism_results.plagiarism_result4 = Plagiarism.run(request.POST.get('answer_4', ''))
        plagiarism_results.plagiarism_result5 = Plagiarism.run(request.POST.get('answer_5', ''))
        plagiarism_results.save()

        # 수정된 내용에 따라 수정된 맞춤법 검사 결과 반영하기
        grammar_results.grammar_result1 = Grammar.run(request.POST.get('answer_1', ''))
        grammar_results.grammar_result2 = Grammar.run(request.POST.get('answer_2', ''))
        grammar_results.grammar_result3 = Grammar.run(request.POST.get('answer_3', ''))
        grammar_results.grammar_result4 = Grammar.run(request.POST.get('answer_4', ''))
        grammar_results.grammar_result5 = Grammar.run(request.POST.get('answer_5', ''))
        grammar_results.save()

        # 수정된 내용에 따라 수정된 합격 & 불합격 결과 반영하기
        pass_results.pass_result1 = '미구현'
        pass_results.pass_result2 = '미구현'
        pass_results.pass_result3 = '미구현'
        pass_results.pass_result4 = '미구현'
        pass_results.pass_result5 = '미구현'
        pass_results.save()

        # 내 자기소개서 페이지(myintro.html)로 이동
        return redirect('/myintro')
    # GET 요청시
    return render(request, 'app/myintroedit.html', {'self_intro' : self_intro, 'username' : username})  # 자기소개서 수정페이지(myintroedit.html) 리턴

# 자기소개서 삭제
def myintro_delete(request, pk):
    self_intro = get_object_or_404(Self_introduction, pk=pk)                # 해당유저 자소서 불러오기, pk는 해당 객체 고유 id값
    plagiarism_results = get_object_or_404(Plagiarism_result, id_value=pk)  # 해당유저 자소서 표절검사 결과 id값을 통해 불러오기
    grammar_results = get_object_or_404(Grammar_result, id_value=pk)        # 해당유저 자소서 맞춤법 검사 결과 id값을 통해 불러오기
    pass_results = get_object_or_404(Grammar_result, id_value=pk)           # 해당유저 자소서 합격 & 불합격 결과 id값을 통해 불러오기

    self_intro.delete()             # 자기소개서 데이터 삭제
    plagiarism_results.delete()     # 표절 검사결과 데이터 삭제
    grammar_results.delete()        # 맞춤법 검사결과 데이터 삭제
    pass_results.delete()           # 합격 & 불합격 결과 데이터 삭제

    # 내 자기소개서 페이지(myintro.html)로 이동
    return redirect('/myintro')
########################################################################################################################


# 자유 게시판(삭제보류, 추후 필요에따라 함수명 바꾸기)
"""
def freeboard(request):
    return render(request, 'app/freeboard.html')
"""

# 글쓰기
def writing(request):
    username = username_passing(request)
    # POST 요청시
    if request.method =='POST':
        # 새 게시글 객체 생성
        new_post = Post.objects.create(
            title=request.POST['title'],
            contents=request.POST['content'],
            writer=User.objects.get(pk=request.session.get('user')),
        )
        all_posts = Post.objects.all().order_by('-id')  # 모든 자유게시판 데이터를 id순으로 가져오기
        paginator = Paginator(all_posts, 10)            # 한 페이지에 10개씩 정렬
        page = int(request.GET.get('p', 1))             # 1번 페이지 값
        posts = paginator.get_page(page)                # 1번 페이지 가져오기
        return redirect('/freeboard')                   # 자유 게시판 페이지로 이동
    # GET 요청시
    return render(request, 'app/writing.html', {'username' : username})     # 글쓰기 페이지(writing.html) 리턴

# 자유게시판
def freeboard_list(request):
    username = username_passing(request)

    all_posts = Post.objects.all().order_by('-id')  # 모든 자유게시판 데이터를 id순으로 가져오기
    paginator = Paginator(all_posts, 10)            # 한 페이지에 10개씩 정렬
    page = int(request.GET.get('p', 1))             # 1번 페이지 값
    posts = paginator.get_page(page)                # 1번 페이지 가져오기
    
    return render(request, 'app/freeboard.html', {'posts' : posts, 'username' : username})  # 자유 게시판 페이지(freeboard.html) 리턴

# 게시글 보기
def post_detail(request, pk):
    username = username_passing(request)
    post = get_object_or_404(Post, pk=pk)

    return render(request, 'app/boarddetail.html', {'post' : post, 'username' : username})  # 게시글 보기 페이지(boarddetail.html) 리턴

# 게시글 수정
# post=Post.objects.get(pk=pk) 주석요청
def post_edit(request, pk):
    username = username_passing(request)
    post=Post.objects.get(pk=pk)                                            # 해당 게시글 테이블 저장

    # POST 요청시
    if request.method=="POST":
        post.title=request.POST['title']                                    # 제목 수정 반영
        post.contents=request.POST['contents']                              # 내용 수정 반영
        post.save()                                                         # 수정된 내용 저장
        return redirect('/freeboard')                                       # 자유 게시판 페이지로 이동
    # GET 요청시
    return render(request, 'app/postedit.html', {'post':post, 'username' : username})   # 게시글 수정 페이지(postedit.html) 리턴

# 게시글 삭제
def post_delete(request, pk):
    post = Post.objects.get(id=pk)                                          # 해당 게시글 테이블 저장
    post.delete()                                                           # 해당 게시글 삭제
    return redirect('/freeboard/')                                          # 자유 게시판 페이지로 이동