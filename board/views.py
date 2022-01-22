
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count
from django.forms import Form
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView, ListView
from django.utils import timezone

from .forms import NewTopicForm, PostForm
from .models import Board, Topic, Post
from django.views import generic


class IndexView(generic.ListView):
    model = Board
    template_name = 'board/home.html'
    context_object_name = 'boards'

    def get_queryset(self):
        """返回所有论坛对象."""
        return Board.objects.all()


# def board_topics(request,pk):
#     board = get_object_or_404(Board, pk=pk)
#     queryset = board.topics.order_by('-last_updated').annotate(replies=Count('posts') - 1)
#     page=request.GET.get('page',1)  #todo
#
#     paginator = Paginator(queryset, 20)
#     try:
#         topics = paginator.page(page)
#     except PageNotAnInteger:
#         # fallback to the first page
#         topics = paginator.page(1)
#     except EmptyPage:
#         # probably the user tried to add a page number
#         # in the url, so we fallback to the last page
#         topics = paginator.page(paginator.num_pages)
#
#     return render(request, 'board/board_topics.html', {'board': board, 'topics': topics})


class TopicListView(ListView):
    """
    使用 GCBV分页显示板块下的所有话题
    """
    model = Topic
    context_object_name = 'topics'
    template_name = 'board/board_topics.html'
    paginate_by = 15

    def get_context_data(self, **kwargs):
        kwargs['board'] = self.board
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.board = get_object_or_404(Board, pk=self.kwargs.get('pk'))
        queryset = self.board.topics.order_by('-last_updated').annotate(replies=Count('posts') - 1)
        return queryset


# class BoardDetailView(generic.DetailView):
#     model = Board  # model 首字母必须小写！
#     template_name = 'board/topics.html'


@login_required
def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = request.user
            topic.last_updated = topic.created_at = timezone.now()
            topic.save()
            post = Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=request.user
            )

            return redirect('board:topic_posts', pk=board.pk, topic_pk=topic.pk)
    else:
        form = NewTopicForm()
    return render(request, 'board/new_topic.html', {'board': board, 'form': form})


# def topic_detail(request, pk, topic_pk):
#     topic = get_object_or_404(Topic, pk=topic_pk)
#     topic.views += 1
#     topic.save()
#     return render(request, 'board/topic_posts.html', {'topic': topic})


class PostListView(ListView):
    Model = Post
    context_object_name = 'posts'
    template_name = 'board/topic_posts.html'
    paginate_by = 15

    def get_context_data(self, **kwargs):
        session_key = 'viewed_topic_{}'.format(self.topic.pk)  # <-- here
        if not self.request.session.get(session_key, False):
            self.topic.views += 1
            self.topic.save()
            self.request.session[session_key] = True

        kwargs['topic'] = self.topic
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.topic = get_object_or_404(Topic, board__pk=self.kwargs.get('pk'), pk=self.kwargs.get('topic_pk'))
        queryset = self.topic.posts.order_by('created_at')
        return queryset


@login_required()
def reply_topic(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()
            topic.last_updated = timezone.now()
            topic.save()
            topic_url = reverse('board:topic_posts', kwargs={'pk': pk, "topic_pk": topic_pk})
            topic_post_url = "{url}?page={page}#{id}".format(  # todo
                url=topic_url,
                id=post.pk,
                page=topic.get_page_count(),
            )
            return redirect(topic_post_url)

    else:
        form = PostForm()
    return render(request, 'board/reply_topic.html', {'topic': topic, 'form': form})


# @method_decorator(login_required, name='dispatch')  #todo  错误信息： get_queryset没有被重写
# class EditPost(UpdateView):
#     Model = Post
#     fields = ('message',)
#     template_name = 'board/edit_post.html'
#     pk_url_kwarg = 'post_pk'
#     context_object_name = 'post'
#
#     def get_queryset(self):
#         queryset = super().get_queryset()
#         return queryset.filter(created_by=self.request.user)
#
#
#     def form_valid(self, form):
#         post = form.save(commit=False)
#         post.created_by = self.request.user
#         post.created_at = timezone.now()
#         post.save()
#         return redirect("board:topic_posts", pk=post.topic.board.pk, topic_pk=post.topic.pk)

@login_required()
def edit_post(request, pk, topic_pk, post_pk):
    post = get_object_or_404(Post, pk=post_pk, created_by=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.updated_at
            Post.objects.filter(pk=post_pk).update(message=post.message, updated_at=timezone.now(),
                                                   updated_by=request.user)
            return redirect("board:topic_posts", pk=pk, topic_pk=topic_pk)
    else:
        form = PostForm()
    if post:
        return render(request, 'board/edit_post.html', {'post': post, 'form': form})
    else:
        raise Http404
