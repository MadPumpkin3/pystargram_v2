from django.shortcuts import render, redirect
from posts.models import Post
from posts.forms import CommentForm
from django.views.decorators.http import require_POST

# Create your views here.
def feeds(request):
    if not request.user.is_authenticated:
        return redirect("/users/login/")
    posts = Post.objects.all()
    comment_form = CommentForm()
    context = {
        "posts": posts,
        "comment_form": comment_form,
        }
    return render(request, "posts/feeds.html", context)

@require_POST
def comment_add(request):
    print(request.POST)