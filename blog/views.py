from django.shortcuts import render, get_object_or_404, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.core.mail import send_mail
from .models import Post, Comment
from .forms import EmailPostForm, CommentForm
from taggit.models import Tag


class PostListView(ListView):
    queryset = posts = Post.objects.all().order_by('publish') #отвечает за ту выборку из базы, с которой будет работать
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'list.html'


# def post_share_view(request, post_id):
#     post = get_object_or_404(Post, id=post_id)
#     if request.method == 'POST':
#         form = EmailPostForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             post_url = request.build_absolute_uri(post.get_absolute_url()) #'TEST URL'
#             subject = '{} ({}) recommends you reading "{}"'.format(cd['name'], cd['email'], post.title)
#             message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title, post_url, cd['name'], cd['comments'])
#             send_mail(subject, message, 'thisisvlados@mail.ru', [cd['to']])
#             sent = True
#     else:
#         form = EmailPostForm()
#         sent = False
#     return render(request,
#                   'share_post.html',
#                   {
#                       'post': post,
#                       'form': form,
#                       'sent': sent
#                   })



#внизу то же самое, что и сверху(в классе)
# def post_list(request):
#     #posts = get_object_or_404(Post, id=1)
#     posts = Post.objects.all().order_by('publish') #забираем все посты (order_by - отбражение постов по порядку)
#     paginator = Paginator(posts, 3) #выбираем, сколько постов будет на странице
#     page = request.GET.get('page') #из запроса достаём номер страницы
#     try:
#         page_posts = paginator.page(page) #получаем все посты на этой странице
#     except PageNotAnInteger:
#         page_posts = paginator.page(1)
#     except EmptyPage:
#         page_posts = paginator.page(paginator.num_pages) #если пустая страница, возвращаемся обранто
#
#     return render(request,
#                   'list.html',
#                   {
#                       'page' : page,
#                       'posts': page_posts
#                   })


def post_list(request, tag_slug=None):
    object_list = Post.objects.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 3) # 3 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request, 'list.html', {'page': page,
                                         'posts': posts,
                                         'tag': tag})

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                                   status='draft',
                                   publish__year=year,
                                   publish__month=month,
                                   publish__day=day)
    comments = post.comments.all()
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()

    else:
        comment_form = CommentForm()


    return render(request,
                  'detail.html',
                  {
                      'post': post,
                      'comments': comments,
                      'comment_form': comment_form
                   }
                  )

