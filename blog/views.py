from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import *
import markdown
from django.views.generic import ListView, DetailView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
from django.db.models import Q
from haystack.views import SearchView
from .forms import *
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    return render(request, 'blog/index.html', context={
    })

#获取前后post
def _get_paginator(post_list, curpost):
    prepost = None
    nextpost = None
    if post_list and curpost:
        paginator = Paginator(post_list, 1)
        index = list(post_list).index(curpost) + 1
        pageobj = paginator.page(index)
        if pageobj.has_previous():
            prepost = post_list[index - 2]
        if pageobj.has_next():
            nextpost = post_list[index]
    return prepost, nextpost

#对文本进行markdown解析
def _markdown_post(post):
    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        TocExtension(slugify=slugify),
    ])
    post.body = md.convert(post.body)
    post.toc = md.toc

#详情类视图
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'curpost'
    
    def get_object(self, queryset=None):
        post = super(PostDetailView, self).get_object(queryset=None)
        _markdown_post(post)
        return post

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        cate = get_object_or_404(Category, pk=self.object.category.pk)
        post_list = Post.objects.filter(category=cate)
        prepost, nextpost = _get_paginator(post_list, self.object)
        comment_list = self.object.comment_set.all()
        context.update({
            'post_list': post_list,
            'closeflag': 1,
            'prepost': prepost,
            'nextpost': nextpost,
            'comment_list': comment_list,
        })
        return context

#分类函数
def category(request):
    catepk = request.GET.get('catepk')
    postpk = request.GET.get('postpk')
    curpost = None
    post_list = None
    closeflag = request.GET.get('closeflag') or 0

    #设置列表关闭状态
    if int(closeflag) == 1:
        closeflag = 0
    else:
        closeflag = 1

    #取分类下的文章列表
    if catepk:
        cate = get_object_or_404(Category, pk=catepk)
        post_list = Post.objects.filter(category=cate)

    #取当前文章
    if postpk:
        curpost = get_object_or_404(Post, pk=postpk)
    elif len(post_list) > 0:
        curpost = post_list[0]

    if curpost:
        _markdown_post(curpost)

    prepost, nextpost = _get_paginator(post_list, curpost)

    return render(request, 'blog/detail.html', context={
        'curpost': curpost,
        'post_list': post_list,
        'closeflag': closeflag,
        'prepost': prepost,
        'nextpost': nextpost,
    })

#搜索
@login_required
def editor(request):
    if request.method == 'POST':
        form = EditorForm(request.POST)

        if form.is_valid():
            post = Post.objects.create(
                title = form.cleaned_data['title'],
                body = form.cleaned_data['body'],
                category_id = form.cleaned_data['category'],
                author = request.user,
            )
            post.save()
            return redirect(post)
    else:
        # 请求不是 POST，表明用户正在访问注册页面，展示一个空的注册表单给用户
        form = EditorForm()

    return render(request, 'blog/editor.html', context={
        'form': form,
    })

class MySearchView(SearchView):
    template = 'blog/search.html'
    '''
    template = 'blog/search_bak.html'

    def get_context(self):
        context = super(MySearchView, self).get_context()
        pk = self.request.GET.get('pk')
        curpost = None
        pageobj = context.get('page')
        if pk:
            curpost = get_object_or_404(Post, pk=pk)
        elif len(pageobj) > 0:
            curpost = pageobj[0].object

        if curpost:
            _markdown_post(curpost)
        context['curpost'] = curpost
        context['q'] = self.request.GET.get('q')
        return context
    '''

'''
#搜索
def search(request):
    q = request.GET.get('q')
    error_msg = ''

    if not q:
        error_msg = "请输入关键词"
        return render(request, 'blog/search.html', {'error_msg': error_msg})

    post_list = Post.objects.filter(Q(title__icontains=q) | Q(body__icontains=q))

    pk = request.GET.get('pk')
    curpost = None
    if pk:
        curpost = get_object_or_404(Post, pk=pk)
    elif len(post_list) > 0:
        curpost = post_list[0]

    if curpost:
        _markdown_post(curpost)

    return render(request, 'blog/search.html', context={
        'error_msg': error_msg,
        'post_list': post_list,
        'curpost': curpost,
        'q': q,
    })
'''