from urllib import request
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q 
from .models import Category, Post, Author, About, Like, Dislike, Comment, Tag, Report, View
from django.contrib import messages 
from django.contrib.auth.decorators import login_required 

def get_author(user):
    qs = Author.objects.filter(user=user)
    if qs.exists():
        return qs[0]
    return None

def homepage (request):
    categories = Category.objects.all()[0:3]
    featured = Post.objects.filter(featured=True)
    latest = Post.objects.order_by('-timestamp')[0:3]
    context= {
        'object_list': featured,
        'latest': latest,
        'categories':categories,
    }
    return render(request, 'homepage.html',context)

def post (request,slug):
    post = Post.objects.get(slug = slug)
    latest = Post.objects.order_by('-timestamp')[:3]
    user = request.user if request.user.is_authenticated else None 
    ip_address = request.META.get('REMOTE_ADDR') 
    View.objects.create(user=user, post=post, ip_address=ip_address) 
    comments = post.comments.all() 
    liked = False 
    if request.user.is_authenticated: 
        liked = post.likes.filter(user=request.user).exists() 
    context = {
        'post': post,
        'latest': latest,
        'liked' : liked,
        'comments': comments, 
    }
    return render(request, 'post.html', context)

def about (request):
    return render(request, 'about_page.html')

def search(request):
    queryset = Post.objects.all()
    query = request.GET.get('q')
    if query:
        queryset = queryset.filter(
            Q(title__icontains=query) |
            Q(overview__icontains=query)
        ).distinct()
    context = {
        'object_list': queryset
    }
    return render(request, 'search_bar.html', context)


def postlist (request,slug):
    category = Category.objects.get(slug = slug)
    posts = Post.objects.filter(categories__in=[category])

    context = {
        'posts': posts,
        'category': category,
    }
    return render(request, 'post_list.html', context)

def allposts(request):
    posts = Post.objects.order_by('-timestamp')

    context = {
        'posts': posts,
    }
    return render(request, 'all_posts.html', context)

def about(request): 
    about = About.objects.first()  # İlk (və yeganə) About obyektini götür 
    context = { 
        'about': about 
    } 
    return render(request, 'about_page.html', context) 

@login_required(login_url='/admin/login/') 
def like_post(request, slug): 
    if request.method == 'POST': 
        post = get_object_or_404(Post, slug=slug) 
         
        if Like.objects.filter(user=request.user, post=post).exists(): 
            Like.objects.filter(user=request.user, post=post).delete() 
        else: 
            Like.objects.create(user=request.user, post=post) 
            Dislike.objects.filter(user=request.user, post=post).delete() 
 
     
    return redirect('post', slug=slug) 

@login_required(login_url='/admin/login/') 
def dislike_post(request, slug): 
    if request.method == 'POST': 
        post = get_object_or_404(Post, slug=slug) 
         
        if Dislike.objects.filter(user=request.user, post=post).exists(): 
            Dislike.objects.filter(user=request.user, post=post).delete() 
        else: 
            Dislike.objects.create(user=request.user, post=post) 
            Like.objects.filter(user=request.user, post=post).delete() 
     
    return redirect('post', slug=slug) 

def add_comment(request, slug): 
    if request.method == 'POST' and request.user.is_authenticated: 
        post = get_object_or_404(Post, slug=slug) 
        content = request.POST.get('content') 
 
        if content: 
            Comment.objects.create( 
                user=request.user, 
                post=post, 
                content=content 
            ) 
 
    return redirect('post', slug=slug) 

def posts_by_tag(request, slug): 
    tag = get_object_or_404(Tag, slug=slug) 
    posts = tag.posts.all() # related_name='posts' olmalıdır Tag modeli ilə 
 
    context = { 
        'tag': tag, 
        'posts': posts, 
    } 
    return render(request, 'posts_by_tag.html', context) 

def report_post(request, slug): 
    """Post-u report etmə səhifəsi""" 
    post = get_object_or_404(Post, slug=slug) 
 
    if request.method == 'POST': 
        reporter_name = request.POST.get('reporter_name') 
        reporter_email = request.POST.get('reporter_email') 
        reason = request.POST.get('reason') 
        description = request.POST.get('description') 
 
        # Əgər eyni email-dən əvvəlcə report varsa 
        existing_report = Report.objects.filter( 
            post=post, 
            reporter_email=reporter_email 
        ).exists() 
 
        if existing_report: 
            messages.warning(request, 'Bu post üçün artıq şikayət vermişsiniz!') 
            return redirect('post', slug=slug) 
 
        # Yeni report yaradın 
        Report.objects.create( 
            post=post, 
            reporter_name=reporter_name, 
            reporter_email=reporter_email, 
            reason=reason, 
            description=description 
        ) 
 
        messages.success(request, 'Şikayətiniz qeydə alındı. Təşəkkür edirik!') 
        return redirect('post', slug=slug) 
 
    context = { 
    'post': post, 
    } 
    return render(request, 'report_post.html', context)