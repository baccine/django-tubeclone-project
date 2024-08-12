from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post, Comment, Tag
from .forms import CommentForm, PostForm



def tube_list(request):
    q = request.GET.get("q", "")
    if q:
        posts = Post.objects.filter(title__icontains=q) | Post.objects.filter(
            content__icontains=q
        )
        return render(request, "tube/tube_list.html", {"posts": posts, "q" : q})
    posts = Post.objects.all()
    return render(request, "tube/tube_list.html", {"posts": posts})

    
def tube_detail(request, pk):
    post = Post.objects.get(pk=pk)
    form = CommentForm()
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            author = request.user
            message = form.cleaned_data["message"]  # 올바른 속성 사용
            c = Comment.objects.create(post=post, author=author, message=message)
            c.save()# 이미 save()를 호출하는 Comment.objects.create 사용함으로 c.save() 불필요
    return render(
        request,
        "tube/tube_detail.html",
        {"post": post, "form": form},
    )
    
@login_required
def tube_create(request):
    if request.method == "GET":
        form = PostForm()
        return render(request, "tube/tube_create.html", {"form": form})
    else:
        form = PostForm(request.POST, request.FILES)
        if form. is_valid():
            post = form.save()
            return redirect("tube_list")
        else:
            form = PostForm()
            return render(request, "tube/tube_create.html", {"form": form})
    
@login_required
def tube_update(request, pk):
    post = get_object_or_404(Post, pk=pk)
    
    if post.author != request.user:
        return redirect("tube_list")
        
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect("tube_detail", pk)
    else:
        form = PostForm(instance=post)
        return render(request, "tube/tube_update.html", {"form":form, "pk" : pk})

@login_required
def tube_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    
    if post.author != request.user:
        return redirect("tube_list")
    
    if request.method == "POST":
        post.delete()
        
    return redirect("tube_list")


def tube_tag(request, tag):
    Posts = Post.objects.filter(tags__name__iexact=tag)
    return render(request, "tube/tube_list.html", {"posts": Posts})