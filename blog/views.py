from django.contrib.auth.decorators import login_required

from django.views import generic
from .models import Post
from .forms import CommentForm, PostForm
from django.shortcuts import render, get_object_or_404

class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'

class PostDetail(generic.DetailView):
    model = Post
    template_name = 'post_detail.html'

def post_detail(request, slug):
    template_name = 'post_detail.html'
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.filter(active=True)
    new_comment = None
    # Comment posted
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():

            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(request, template_name, {'post': post,
                                           'comments': comments,
                                           'new_comment': new_comment,
                                           'comment_form': comment_form})

@login_required
def new_post(request):
    """Render the page to create a new post."""
    current_user = request.user

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()

    else:
        form = PostForm(initial={'author': current_user})

    context = {'form': form}
    return render(request, 'new_post.html', context)
