from django.shortcuts import redirect

# 사용자 로그인 여부에 따른 페이지 자동 전환 로직
def index(request):
    if request.user.is_authenticated:
        return redirect("posts:feeds")
    else:
        return redirect("users:login")