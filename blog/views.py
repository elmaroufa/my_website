import imp
from re import template
from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Post
from .forms import CommentForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

# Create your views here.


#class PostList(generic.ListView):
#    queryset = Post.objects.filter(status=1).order_by('-created_on')
#    template_name = 'index.html'

#class PostDetail(generic.DetailView):
#   model = Post
#    template_name = 'post_detail.html'

def post_list(request):
    object_list = Post.objects.filter(status=1).order_by('-created_on')
    page_num = request.GET.get('page', 1)
    paginator = Paginator(object_list, 4)

    try:
        page_obj = paginator.page(page_num)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return render(request, 'index.html', {'page_obj' : page_obj})


def post_detail(request, slug):
    template_name = 'post_detail.html'
    post = get_object_or_404(Post, slug=slug)
    print(dir(post))
    comments = post.comments.filter(active=True)
    new_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()
    return render(request,template_name, {
                'post' : post,
                'comments': comments,
                'new_comment' : new_comment,
                'comment_form' : comment_form
            })

def portofolio_view(request):
    template_name = 'portofolio.html'
    return render(request,template_name)




