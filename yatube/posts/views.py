from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

from .models import Group, Post, User, Follow
from .forms import PostForm, CommentForm
from yatube.settings import PAGINATOR_OBJECTS_PER_PAGE as per_page
from yatube.settings import PAGINATOR_COMMENT_PER_PAGE as per_page_comment


def get_page_object(request, posts):
    paginator = Paginator(posts, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj


def get_users(request, username):
    follower = get_object_or_404(User, username=request.user)
    following = get_object_or_404(User, username=username)
    return follower, following


def index(request):
    template = 'posts/index.html'
    posts = Post.objects.all()
    page_obj = get_page_object(request, posts)
    context = {
        'title': 'Главная страница',
        'page_obj': page_obj,
    }
    return render(request, template, context)


def group_posts(request, slug):
    template = 'posts/group_list.html'
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()
    page_obj = get_page_object(request, posts)
    context = {
        'page_obj': page_obj,
        'title': group,
    }
    return render(request, template, context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    posts = author.posts.all()
    page_obj = get_page_object(request, posts)
    context = {
        'page_obj': page_obj,
        'author': author,
        'count_posts': posts.count(),
        'title': f'Профайл пользователя {author}',
        'following': False
    }
    if request.user.is_authenticated:
        if Follow.objects.filter(user=request.user,
                                 author=author).exists():
            context['following'] = True

    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    form = CommentForm(request.POST or None)
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()
    count_posts = post.author.posts.count()
    paginator = Paginator(comments, per_page_comment)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'form': form,
        'title': post.text[:30],
        'post': post,
        'count_posts': count_posts,
        'page_obj': page_obj,
        'paginator': paginator
    }
    return render(request,
                  'posts/post_detail.html',
                  context)


@login_required
def post_create(request):
    form = PostForm(request.POST or None,
                    files=request.FILES or None, )

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


@login_required
def add_comment(request, post_id):
    form = CommentForm(request.POST or None)
    post = get_object_or_404(Post,
                             id=post_id)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect(reverse('posts:post_detail',
                            args=[post_id]))


@login_required
def follow_index(request):
    follower = get_object_or_404(User, username=request.user)
    following_list = Follow.objects.filter(user=follower).values('author')
    posts = Post.objects.filter(author_id__in=following_list)
    page_obj = get_page_object(request, posts)

    context = {
        'page_obj': page_obj,
        'title': 'Страница подписок',
    }
    return render(request, 'posts/follow.html', context)


@login_required
def profile_follow(request, username):
    follower, following = get_users(request, username)
    if request.user != following:
        Follow.objects.get_or_create(user=follower,
                                     author=following)
    return redirect(reverse('posts:profile',
                            args=[username]))


@login_required
def profile_unfollow(request, username):
    follower, following = get_users(request, username)
    follow_obj = Follow.objects.filter(user=follower,
                                       author=following)
    follow_obj.delete()
    return redirect(reverse('posts:profile',
                            args=[username]))
