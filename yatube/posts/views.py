from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

from .models import Group, Post, User
from .forms import PostForm
from yatube.settings import PAGINATOR_OBJECTS_PER_PAGE as per_page


def index(request):
    template = 'posts/index.html'
    posts = Post.objects.all()
    paginator = Paginator(posts, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'title': 'Главная страница',
        'page_obj': page_obj,
        'paginator': paginator
    }
    return render(request, template, context)


def group_posts(request, slug):
    template = 'posts/group_list.html'
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()
    paginator = Paginator(posts, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'paginator': paginator,
        'page_obj': page_obj,
        'title': group,
    }
    return render(request, template, context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    posts = author.posts.all()
    paginator = Paginator(posts, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'author': author,
        'count_posts': posts.count(),
        'title': f'Профайл пользователя {author}'
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    count_posts = post.author.posts.count()
    context = {
        'title': post.text[:30],
        'post': post,
        'count_posts': count_posts
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    form = PostForm(request.POST or None)

    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect(reverse('posts:profile',
                                args=[post.author]))

    context = {
        'title': 'Новый пост',
        'form': form,
    }
    return render(request, 'posts/create_post.html', context)


@login_required
def post_edit(request, post_id):
    is_edit = True
    post = get_object_or_404(Post, id=post_id)
    form = PostForm(request.POST or None, instance=post)
    if form.is_valid():
        form.save()
        return redirect(reverse('posts:post_detail',
                                args=[post_id]))

    context = {
        'form': form,
        'is_edit': is_edit,
        'title': 'Редактирование поста'
    }

    return render(request, 'posts/create_post.html', context)
