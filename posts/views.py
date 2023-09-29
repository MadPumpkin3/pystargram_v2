from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponseForbidden
from posts.models import Post, Comment, PostImage
from posts.forms import CommentForm, PostForm
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
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        
        comment.user = request.user
        
        comment.save()
        
        print(comment.id)
        print(comment.content)
        print(comment.user)
        
        return HttpResponseRedirect(f"/posts/feeds/#post-{comment.post.id}")
    
@require_POST
def comment_delete(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    if comment.user == request.user:
        comment.delete()
        return HttpResponseRedirect(f"/posts/feeds/#psot-{comment.post.id}")
    else:
        return HttpResponseForbidden("이 댓글을 삭제할 권한이 없습니다")
        
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
            
            url = f"/posts/feeds/#post-{post.id}"
            return HttpResponseRedirect(url)
    
    else:
        form = PostForm()
    
    context = {"form": form}
    return render(request, "posts/post_add.html", context)