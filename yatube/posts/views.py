from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .models import Post, Group, User
from .forms import PostForm
from .paginator import pagination


def index(request):
    post_list = Post.objects.all()
    page_obj = pagination(request, post_list, settings.POSTS_NUM)
    return render(request, 'posts/index.html', {'page_obj': page_obj})


def group_posts(request, slug: str):
    group = get_object_or_404(Group, slug=slug)
    post_list = Post.objects.filter(group=group)
    page_obj = pagination(request, post_list, settings.POSTS_NUM)
    return render(request, 'posts/group_list.html', {'group': group,
                                                     'page_obj': page_obj})


def profile(request, username: str):
    user = User.objects.get(username=username)
    post_list = Post.objects.filter(author=user)
    page_obj = pagination(request, post_list, settings.POSTS_NUM)
    context = {
        'username': user,
        'page_obj': page_obj,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id: int):
    post = Post.objects.get(pk=post_id)
    context = {
        'post': post,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            user = request.user
            form.instance.author = user
            form.save()
            return redirect(f'/profile/{user.username}/')
        return render(request, 'posts/create_post.html', {'form': form})
    form = PostForm()
    return render(request, 'posts/create_post.html', {'form': form})


@login_required
def post_edit(request, post_id: int):
    post = get_object_or_404(Post, pk=post_id)
    if post.author == request.user:
        form = PostForm(request.POST or None, instance=post)
        if form.is_valid():
            form.instance.author = request.user
            form.save()
            return redirect('posts:post_detail', post_id)
        return render(request, 'posts/create_post.html', {'form': form,
                                                          'post': post,
                                                          'is_edit': True})
    else:
        form = PostForm()
        return render(request, 'posts/create_post.html', {'form': form})
