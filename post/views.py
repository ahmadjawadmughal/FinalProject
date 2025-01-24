from django.shortcuts import render, redirect, get_object_or_404
from .models import Post
from django.db.models import Q
from comment.models import Comment
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import PostForm
from comment.forms import CommentForm
import requests
from django.core.paginator import Paginator
# Create your views here.

@login_required
def create_post(request):
    if request.method == "POST" and request.user.is_authenticated:

        form = PostForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()

            messages.success(request, "Your post is created!")
        return redirect("list-post")
    else:
        form = PostForm()
        return render(request, "forms.html", {'form': form})


@login_required
def update_post(request, id):

    post = get_object_or_404(Post,id = id, user= request.user)

    if request.method == "POST" and request.user.is_authenticated:
        form = PostForm(request.POST, instance=post)

        if form.is_valid():
            form.save()

            messages.success(request, "Post is updated!")
            return redirect("list-post")
        
        else:
            messages.error(request, "Updating the Post data is failed!")
    form = PostForm(instance=post)
    return render(request, "forms.html", {'form': form})    



@login_required
def delete_post(request, id):
    
    post = get_object_or_404(Post, id = id, user = request.user)
    if request.method == "POST" and request.user.is_authenticated:
        post.delete()
        messages.success(request, f"{post.title} is deleted successfully!")
        return redirect("list-post")
    
    return render(request, "confirm_delete.html", {'post': post})



def fetch_posts():
    try:
        # if not Post.objects.exists():
            response = requests.get("https://jsonplaceholder.typicode.com/posts")
            if response.status_code == 200:
                post_data = response.json()
                # Post.objects.all().delete()
                for post in post_data:
                    Post.objects.get_or_create(
                        id = post['id'],
                        # title = post["title"],
                        # content = post["body"],
                        defaults={
                             "title" : post["title"],
                             "content" : post["body"]
                         }
                    )
                    
    except requests.RequestException as e:
        messages.error(requests, f"Error while fetching post: {e}.")


@login_required
def list_post(request):

    fetch_posts()
    posts = Post.objects.all().order_by("-created_at")

    page_num = request.GET.get("page", 1)
    paginator = Paginator(posts, 5)
    page_obj = paginator.get_page(page_num)

    return render(request, "list_post.html", {'posts': posts, 'page_obj': page_obj})


@login_required
def search(request):
    if request.method == "GET":
        query = request.GET.get('search', '')
        posts = Post.objects.all()
        
        if query:
            posts = posts.filter(Q(title__icontains=query) | Q(content__icontains=query)) 
        else:
            messages.info(request, "Please enter a search term.")
            return render(request, "search.html", {'query': query, 'page_obj': None})
        page_num = request.GET.get("page", 1)
        paginator = Paginator(posts, 5)
        page_obj = paginator.get_page(page_num)

        return render(request, "search.html", {'query': query, 'page_obj': page_obj})


@login_required
def my_post(request):
    if request.method == "GET":
        user = request.user
        posts = Post.objects.filter(user=user)
        
        if not posts:
            messages.warning(request, f"{user.username}! Don't have any post yet.")
        else:
            return render(request, "my_post.html", {'posts': posts})    
    return redirect("home")    