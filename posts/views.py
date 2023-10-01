from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponseForbidden
from posts.models import Post, Comment, PostImage, HashTag
from posts.forms import CommentForm, PostForm
from django.views.decorators.http import require_POST
from django.urls import reverse

# Create your views here.
# 피드 조회 로직
def feeds(request):
    if not request.user.is_authenticated:
        return redirect("users:login")
    posts = Post.objects.all()
    comment_form = CommentForm()
    context = {
        "posts": posts,
        "comment_form": comment_form,
        }
    return render(request, "posts/feeds.html", context)

# 댓글 생성 로직
@require_POST
def comment_add(request):
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.save()
        url = reverse("posts:feeds") + f"#post-{comment.post.id}"
        return HttpResponseRedirect(url)
    
# 댓글 삭제 로직
@require_POST
def comment_delete(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    if comment.user == request.user:
        comment.delete()
        url = reverse("posts:feeds") + f"#post-{comment.post.id}"
        return HttpResponseRedirect(url)
    else:
        return HttpResponseForbidden("이 댓글을 삭제할 권한이 없습니다")
        
# 포스트 생성 로직
def post_add(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            
            for image_file in request.FILES.getlist("images"):
                PostImage.objects.create(
                    post=post,
                    photo = image_file,
                )
            
            url = reverse("posts:feeds") + f"#post-{post.id}"
            return HttpResponseRedirect(url)
    
    else:
        form = PostForm()
    
    context = {"form": form}
    return render(request, "posts/post_add.html", context)

def tags(request, tag_name):
    try:
        tag = HashTag.objects.get(name=tag_name)
    except HashTag.DoesNotExist:
        posts = Post.objects.none()
    else:
        posts = Post.objects.filter(tags=tag)
    
    context = {
        "tag_name": tag_name,
        "posts": posts,
    }
    return render(request, 'posts/tags.html', context)