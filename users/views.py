from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from users.forms import LoginForm, SignupForm
from users.models import User

# Create your views here.
# 로그인 로직
def login_view(request):
    if request.user.is_authenticated:
        return redirect("posts:feeds")
    
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            
            user = authenticate(username=username, password=password)
            
            if user:
                login(request, user)
                return redirect("posts:feeds")
            else:
                form.add_error(None, "입력한 자격증명에 해당하는 사용자가 없습니다")
        
        context = {"form": form}
        return render(request, "users/login.html", context)
    else:
        form = LoginForm()
        context = {"form": form}
        return render(request, "users/login.html", context)
# 로그아웃 로직
def logout_view(request):
    logout(request)
    
    return redirect("users:login")
# 회원가입 로직
def signup(request):
    if request.method == "POST":
        form = SignupForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("posts:feeds")
        
    else:
        form = SignupForm()
        
    context = {"form": form}
    return render(request, "users/signup.html", context)

def profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    context = {
        "user": user,
    }
    return render(request, "users/profile.html", context)

def followers(request, user_id):
    user = get_object_or_404(User, id=user_id)
    relationships = user.follower_relationships.all()
    context = {
        "user": user,
        "relationships": relationships,
    }
    return render(request, "users/followers.html", context)

def following(request, user_id):
    user = get_object_or_404(User, id=user_id)
    relationships = user.following_relationships.all()
    context = {
        "user": user,
        "relationships": relationships,
    }
    return render(request, "users/following.html", context)

def follow(request, user_id):
    # 로그인한 유저
    user = request.user
    # 팔로우하려는 유저
    target_user = get_object_or_404(User, id=user_id)
    # 팔로우하려는 유저가 이미 자신의 팔로잉 목록에 있는 경우
    if target_user in user.following.all():
        user.following.remove(target_user)
        
    # 팔로우하려는 유저가 자신의 팔로우 목록에 없는 경우
    else:
        user.following.add(target_user)
        
    # 팔로우 토글 후 이동할 url이 전달되었다면 해당 주소로,
    # 전달되지 않았다면 로그인 한 유저의 프로필 페이지로 이동
    url_next = request.GET.get("next") or reverse("users:profile", args=[user.id])
    return HttpResponseRedirect(url_next)