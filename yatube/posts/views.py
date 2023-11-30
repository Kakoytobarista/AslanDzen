from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from enums import HtmlPathEnum
from .models import Group, Post, User, Follow
from .forms import PostForm, CommentForm
from .utils import get_users


class IndexView(ListView):
    model = Post
    template_name = HtmlPathEnum.INDEX_PAGE.value
    paginate_by = 10


class GroupView(ListView):
    template_name = HtmlPathEnum.GROUP_PAGE.value
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['group'] = get_object_or_404(Group, slug=self.kwargs.get('slug'))
        return context

    def get_queryset(self, *args, **kwargs):
        group = get_object_or_404(Group, slug=self.kwargs.get('slug'))
        posts = group.posts.all()
        return posts


class ProfileView(ListView):
    model = Post
    template_name = HtmlPathEnum.PROFILE_PAGE.value
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        author = get_object_or_404(User,
                                   username=self.kwargs.get('username'))
        posts = author.posts.all()
        context['author'] = author
        context['page_obj'] = posts
        context['count_posts'] = posts.count()
        context['following'] = False
        if self.request.user.is_authenticated:
            if Follow.objects.filter(user=self.request.user,
                                     author=author).exists():
                context['following'] = True
        return context


class PostDetailView(DetailView):
    template_name = HtmlPathEnum.POST_DETAIL_PAGE.value

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = get_object_or_404(Post, id=self.kwargs.get('post_id'))
        comments = post.comments.all()
        form = CommentForm(self.request.POST or None)
        context['form'] = form
        context['post'] = post
        context['page_obj'] = comments
        return context

    def get_object(self, *args, **kwargs):
        post = get_object_or_404(Post, id=self.kwargs.get('post_id'))
        return post


class PostCreateView(CreateView, LoginRequiredMixin):
    model = Post
    template_name = HtmlPathEnum.POST_CREATE_EDIT_PAGE.value
    form_class = PostForm

    def get_success_url(self):
        return reverse('posts:profile', args=[self.request.user])

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.save()
        return super().form_valid(form)


class PostEditView(UpdateView, LoginRequiredMixin):
    model = Post
    template_name = HtmlPathEnum.POST_CREATE_EDIT_PAGE.value
    pk_url_kwarg = 'post_id'
    fields = '__all__'

    def get_success_url(self):
        return reverse('posts:profile', args=[self.request.user])


class PostDeleteView(DeleteView, LoginRequiredMixin):
    model = Post
    pk_url_kwarg = 'post_id'

    def get_success_url(self):
        success_url = str(reverse_lazy('posts:index'))
        return success_url

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class CommentView(CreateView, LoginRequiredMixin):
    model = Post
    form_class = CommentForm

    def get_success_url(self):
        success_url = str(reverse_lazy('posts:post_detail',
                                       args=[self.kwargs.get('post_id')]))
        return success_url

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.post_id = self.kwargs.get('post_id')
        comment.author = self.request.user
        comment.save()
        return super().form_valid(form)


class FollowIndexView(ListView, LoginRequiredMixin):
    model = Post
    template_name = HtmlPathEnum.FOLLOW_PAGE.value
    paginate_by = 10

    def get_queryset(self):
        follower = get_object_or_404(User, username=self.request.user)
        following_list = Follow.objects.filter(user=follower).values('author')
        posts = Post.objects.filter(author_id__in=following_list)
        return posts


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
