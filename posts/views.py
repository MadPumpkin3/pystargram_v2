from django.shortcuts import render, redirect
from posts.models import Post

# Create your views here.
def feeds(request):
    if not request.user.is_authenticated:
        return redirect("/users/login/")
    posts = Post.objects.all()
    context = {"posts": posts}
    return render(request, "posts/feeds.html", context)